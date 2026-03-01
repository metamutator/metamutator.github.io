#!/usr/bin/env python3
"""
Convert SBV (SubViewer) subtitle files to SRT (SubRip) format.
"""

import sys
import os

def convert_timestamp(sbv_timestamp):
    """Convert SBV timestamp format to SRT format."""
    # SBV format: 0:00:01.000,0:00:05.000
    # SRT format: 00:00:01,000 --> 00:00:05,000
    
    start_time, end_time = sbv_timestamp.split(',')
    
    # Pad hours with leading zero if needed
    start_time = start_time.zfill(10)  # Ensures format like 00:00:01.000
    end_time = end_time.zfill(10)
    
    # Replace decimal point with comma for milliseconds (SRT format)
    start_time = start_time.replace('.', ',')
    end_time = end_time.replace('.', ',')
    
    return f"{start_time} --> {end_time}"

def sbv_to_srt(sbv_content):
    """Convert SBV content to SRT format."""
    lines = sbv_content.strip().split('\n')
    srt_content = []
    subtitle_number = 1
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Check if line contains timestamp (SBV format)
        if ',' in line and ':' in line:
            timestamp = line
            subtitle_text = []
            
            # Get subtitle text (everything until next timestamp or end)
            i += 1
            while i < len(lines) and not (lines[i].strip() and ',' in lines[i] and ':' in lines[i]):
                if lines[i].strip():  # Skip empty lines
                    subtitle_text.append(lines[i].strip())
                i += 1
            
            if subtitle_text:  # Only add if there's actual text
                srt_content.append(str(subtitle_number))
                srt_content.append(convert_timestamp(timestamp))
                srt_content.extend(subtitle_text)
                srt_content.append('')  # Empty line between subtitles
                subtitle_number += 1
        else:
            i += 1
    
    return '\n'.join(srt_content)

def main():
    if len(sys.argv) != 2:
        print("Usage: python sbv_to_srt.py <input_file.sbv>")
        print("Output will be saved as <input_file.srt>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    
    # Generate output filename
    base_name = os.path.splitext(input_file)[0]
    output_file = f"{base_name}.srt"
    
    try:
        # Read SBV file
        with open(input_file, 'r', encoding='utf-8') as f:
            sbv_content = f.read()
        
        # Convert to SRT
        srt_content = sbv_to_srt(sbv_content)
        
        # Write SRT file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(srt_content)
        
        print(f"Successfully converted '{input_file}' to '{output_file}'")
        
    except (IOError, UnicodeDecodeError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
