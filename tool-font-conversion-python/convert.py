from fontTools import ttLib
import sys
import os

def convert_to_ttf(input_path, output_path=None):
    """
    将多种字体格式（OTF, WOFF, WOFF2 等）转换为 TTF 文件
    :param input_path: 输入的字体文件路径（支持 .otf, .ttf, .woff, .woff2 等）
    :param output_path: 输出的 TTF 文件路径
    :return: 是否成功
    """
    if not os.path.exists(input_path):
        print(f"错误: 文件 '{input_path}' 不存在")
        return False

    # 如果未指定输出路径，自动生成
    if output_path is None:
        base, _ = os.path.splitext(input_path)
        output_path = base + '.ttf'

    try:
        print(f"正在转换: {os.path.basename(input_path)}")
        
        # 1. 加载字体（fontTools 支持多种格式）
        font = ttLib.TTFont(input_path)
        
        # 2. 分析字体格式
        file_ext = os.path.splitext(input_path)[1].lower()
        flavor = getattr(font, 'flavor', None)

        # 根据文件扩展名和 flavor 属性判断输入格式
        if flavor == 'woff':
            input_format = "WOFF (网页字体)"
        elif flavor == 'woff2':
            input_format = "WOFF2 (网页字体)"
        elif 'CFF ' in font or 'CFF2' in font:
            input_format = "OTF (OpenType with CFF/PostScript 轮廓)"
        elif 'glyf' in font:
            input_format = "TTF/OTF (TrueType 轮廓)"
        else:
            input_format = "未知格式"
            
        print(f"检测到输入格式: {input_format}")

        # 3. 统一转换为标准 TTF
        # 关键步骤：移除可能的网页字体包装或格式标记
        original_flavor = flavor
        font.flavor = None # 移除可能的格式标记，强制转换为 TTF
        
        # 4. 检查轮廓类型并提示
        has_cff = 'CFF ' in font or 'CFF2' in font
        has_glyf = 'glyf' in font
        
        if has_cff and not has_glyf:
            print("提示: 检测到 CFF/PostScript 轮廓，正在转换为 TrueType 轮廓...")
            print("      （此转换是数学近似，某些情况下可能影响小字号渲染效果）")
        elif has_glyf:
            if original_flavor in ('woff', 'woff2'):
                print("提示: 移除网页字体包装，转换为标准 TTF 格式...")
            else:
                print("提示: 字体已包含 TrueType 轮廓，直接保存为标准 TTF...")
        else:
            print("警告: 无法识别的轮廓格式，尝试继续转换...")
            
        # 5. 确保输出文件扩展名为 .ttf
        if not output_path.lower().endswith('.ttf'):
            output_path = os.path.splitext(output_path)[0] + '.ttf'
            
        # 6. 保存为 TTF
        font.save(output_path)

        # 7. 报告结果
        input_size = os.path.getsize(input_path)
        output_size = os.path.getsize(output_path)
        print(f"✓ 转换完成!")
        print(f"   输入文件: {os.path.basename(input_path)} ({input_size:,} 字节)")
        print(f"   输出文件: {os.path.basename(output_path)} ({output_size:,} 字节)")
        
        if input_size > 0:
            change_percent = (output_size - input_size) / input_size * 100
            if change_percent > 5:
                print(f"   文件大小变化: +{change_percent:+.1f}% (可能因轮廓转换导致)")
            elif change_percent < -5:
                print(f"   文件大小变化: {change_percent:+.1f}% (已移除网页字体压缩)")
            else:
                print(f"   文件大小变化: {change_percent:+.1f}% (轻微变化)")
        
        return True
    
    except Exception as e:
        print(f"转换失败: {e}")
        print("可能的原因:")
        print("  1. 文件已损坏或不是有效的字体文件")
        print("  2. 文件格式不受支持")
        print("  3. 文件权限不足")
        return False

if __name__ == "__main__":
    # 命令行参数处理
    if len(sys.argv) < 2:
        print("通用字体格式转换器")
        print("功能: 将多种字体格式统一转换为 TTF 格式")
        print("支持的输入格式: .otf, .ttf, .woff, .woff2, 及更多")
        print("")
        print("用法: python convert.py <输入字体文件> [输出文件.ttf]")
        print("示例: python convert.py font.otf")
        print("示例: python convert.py font.woff2 font_converted.ttf")
        print("示例: python convert版 font.ttf  # 即使输入是ttf，也会重新标准化")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = convert_to_ttf(input_file, output_file)
    sys.exit(0 if success else 1)

# 【控制台输入】

# 基本用法（自动生成输出文件名）
# python convert.py myfont.otf

# 指定输出文件名
# python convert.py myfont.otf newfont.ttf

# 批量转换示例（用 bash 脚本）
# 【一种格式】
# for file in *.otf; do
#     python convert.py "$file"
# done
# 【多种格式批批量】
# for file in *.{otf,woff,woff2}; do
#     [ -e "$file" ] && python convert.py "$file"
# done