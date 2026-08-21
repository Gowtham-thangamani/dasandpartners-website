#!/usr/bin/env python3
"""
Script to remove specific sections from index.html
"""

import re

def remove_sections_from_index():
    file_path = '/var/www/dasandpartners/templates/index.html'
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Define sections to remove with their start and end patterns
    sections_to_remove = [
        # 1. Engineering Excellence in the UAE section
        {
            'start': r'<div class="section-badge mb-3">\s*<span class="badge bg-success-subtle text-success px-4 py-2 rounded-pill[^>]*>\s*<i class="fas fa-star me-2"></i>Engineering Excellence in the UAE\s*</span>\s*</div>',
            'end': r'</div>\s*</div>\s*</div>\s*<!-- Key Stats Cards -->'
        },
        # 2. Trusted by Industry Leaders section
        {
            'start': r'<h3 class="text-center mb-4"[^>]*>\s*<i class="fas fa-award me-2"></i>Trusted by Industry Leaders\s*</h3>',
            'end': r'</div>\s*</div>\s*</div>\s*</div>\s*<!-- Geographic Footprint -->'
        },
        # 3. Strong Geographic Footprint Across UAE section
        {
            'start': r'<h3 class="text-center mb-4"[^>]*>\s*<i class="fas fa-map-marker-alt me-2"></i>Strong Geographic Footprint Across UAE\s*</h3>',
            'end': r'</div>\s*</div>\s*</div>\s*<!-- Services Overview -->'
        },
        # 4. Comprehensive Engineering Services section
        {
            'start': r'<h3 class="text-center mb-4"[^>]*>\s*<i class="fas fa-cogs me-2"></i>Comprehensive Engineering Services\s*</h3>',
            'end': r'</div>\s*</div>\s*</div>\s*<!-- Project Types & Sectors -->'
        },
        # 5. Project Types & Key Sectors section
        {
            'start': r'<!-- Project Types & Sectors -->\s*<div class="row g-4 mb-5">',
            'end': r'</div>\s*</div>\s*<!-- Specialized Structural Expertise -->'
        },
        # 6. Specialized Structural Expertise section
        {
            'start': r'<h3 class="text-center mb-4"[^>]*>\s*<i class="fas fa-tools me-2"></i>Specialized Structural Expertise\s*</h3>',
            'end': r'</div>\s*</div>\s*</div>\s*<!-- Latest Insights & Updates -->'
        }
    ]
    
    # Remove each section
    for section in sections_to_remove:
        # Create a pattern that matches from start to end
        pattern = section['start'] + r'.*?' + section['end']
        
        # Remove the section (using DOTALL flag to match across lines)
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # Clean up any extra whitespace
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Sections removed successfully!")
    print("Removed sections:")
    print("- Engineering Excellence in the UAE")
    print("- Trusted by Industry Leaders") 
    print("- Strong Geographic Footprint Across UAE")
    print("- Comprehensive Engineering Services")
    print("- Project Types")
    print("- Key Sectors")
    print("- Specialized Structural Expertise")

if __name__ == '__main__':
    remove_sections_from_index()




