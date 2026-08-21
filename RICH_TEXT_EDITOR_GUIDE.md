# 📝 Rich Text Editor Guide

## What's New?

Your news and blog content editor now has **CKEditor** - a professional rich text editor just like WordPress! You can now:

✅ **Add Anchor Tags** - Create internal links within articles  
✅ **Format Text** - Bold, italic, underline, headings, lists  
✅ **Insert Links** - Add external and internal links  
✅ **Add Images** - Upload and insert images directly in content  
✅ **Create Tables** - Build data tables  
✅ **Change Colors** - Customize text and background colors  
✅ **Add Special Characters** - Insert symbols and special characters  

---

## 🎯 How to Add Anchor Tags (Table of Contents)

Anchor tags let readers jump to specific sections in your article. Here's how:

### Step 1: Add Headings to Your Content
When writing your blog/news, use heading tags:
```html
<h2>Introduction</h2>
<p>Your introduction text...</p>

<h2>Main Section</h2>
<p>Your main content...</p>

<h2>Conclusion</h2>
<p>Your conclusion...</p>
```

### Step 2: Add Anchors Using the Editor

1. **Select the heading text** you want to link to
2. Click the **"Anchor"** button in the toolbar (looks like a flag 🚩)
3. Give it a unique name (e.g., "introduction", "main-section", "conclusion")
4. Click OK

### Step 3: Create Links to Your Anchors

1. Type the text you want to be clickable (e.g., "Jump to Introduction")
2. Select that text
3. Click the **"Link"** button 🔗
4. In the URL field, type: `#introduction` (# + your anchor name)
5. Click OK

### Example: Creating a Table of Contents

```html
<h3>Table of Contents</h3>
<ul>
  <li><a href="#introduction">Introduction</a></li>
  <li><a href="#main-section">Main Section</a></li>
  <li><a href="#conclusion">Conclusion</a></li>
</ul>

<h2 id="introduction">Introduction</h2>
<p>Your introduction text here...</p>

<h2 id="main-section">Main Section</h2>
<p>Your main content here...</p>

<h2 id="conclusion">Conclusion</h2>
<p>Your conclusion here...</p>
```

---

## 🎨 Editor Toolbar Features

### Text Formatting
- **Bold** - Make text bold
- **Italic** - Make text italic
- **Underline** - Underline text
- **Strike** - Strikethrough text
- **Subscript/Superscript** - For formulas (H₂O, x²)

### Lists & Alignment
- **Numbered List** - 1, 2, 3...
- **Bullet List** - • • •
- **Indent/Outdent** - Adjust list levels
- **Align Left/Center/Right/Justify** - Text alignment
- **Blockquote** - Highlight important quotes

### Links & Media
- **Link** 🔗 - Add hyperlinks
- **Unlink** - Remove links
- **Anchor** 🚩 - Create jump points
- **Image** 🖼️ - Insert images
- **Table** - Create tables
- **Horizontal Rule** - Add dividers

### Formatting Options
- **Styles** - Apply pre-defined styles
- **Format** - Choose paragraph/heading types (H1, H2, H3, etc.)
- **Font** - Change font family
- **Font Size** - Adjust text size
- **Text Color** - Change text color
- **Background Color** - Highlight text

### Utilities
- **Undo/Redo** - Go back/forward
- **Source** - View/edit HTML code
- **Maximize** - Fullscreen editing

---

## 💡 Pro Tips

### 1. Using Headings for SEO
Use headings properly for better SEO:
- **H1** - Only for the main title (auto-added from title field)
- **H2** - Major sections
- **H3** - Subsections
- **H4** - Minor points

### 2. Creating Professional Content

**Good Structure:**
```html
<h2>What is Django?</h2>
<p>Django is a high-level Python web framework...</p>

<h3>Key Features</h3>
<ul>
  <li>Fast development</li>
  <li>Secure by default</li>
  <li>Scalable</li>
</ul>

<h2>Getting Started</h2>
<p>To start with Django...</p>
```

### 3. Adding Images

1. Click the **Image** button
2. Click **Browse Server** or **Upload** tab
3. Select your image
4. Add **Alternative Text** (important for SEO and accessibility)
5. Set **Width** if needed (recommended: max 800px)
6. Click OK

### 4. Creating Responsive Tables

```html
<table border="1" style="width:100%">
  <thead>
    <tr>
      <th>Feature</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>MEP Services</td>
      <td>Mechanical, Electrical, and Plumbing</td>
    </tr>
    <tr>
      <td>BIM Services</td>
      <td>Building Information Modeling</td>
    </tr>
  </tbody>
</table>
```

### 5. Adding Call-to-Action Sections

```html
<div style="background-color:#148255;color:white;padding:30px;border-radius:15px;text-align:center;margin:30px 0;">
  <h3 style="color:white;margin-bottom:15px;">Need Engineering Consultation?</h3>
  <p>Contact our experts today for a free consultation.</p>
  <a href="/contact-us" style="background:white;color:#148255;padding:12px 30px;border-radius:25px;text-decoration:none;display:inline-block;margin-top:15px;font-weight:600;">
    Contact Us
  </a>
</div>
```

---

## 🚀 Quick Start Workflow

1. **Write your title** in the title field
2. **Add a brief excerpt** (shown in previews)
3. **In the content editor:**
   - Write your introduction
   - Add headings for each section (H2, H3)
   - Insert images where needed
   - Add links to relevant pages
   - Create anchor tags for long articles
4. **Preview using "Source"** button to check HTML
5. **Save your post**

---

## 🔍 SEO Best Practices

### 1. Use Keywords in Headings
```html
<h2>MEP Engineering Services in Dubai</h2>
```

### 2. Add Alt Text to Images
Always describe images for accessibility and SEO

### 3. Internal Linking
Link to other blog posts and pages on your website

### 4. Break Up Content
Use headings, lists, and images to make content scannable

### 5. Add Call-to-Actions
Guide readers to contact you or read related articles

---

## 🎓 Advanced: HTML View

Click the **"Source"** button to switch to HTML view. This is useful for:

- Adding custom styling
- Copying content from other sources
- Fine-tuning layout
- Adding advanced elements like accordions or tabs

### Example: Custom Styled Box
```html
<div style="border-left:4px solid #148255;background:#f8f9fa;padding:20px;margin:20px 0;">
  <strong>Pro Tip:</strong> Always consider energy efficiency in MEP design!
</div>
```

---

## 🆘 Troubleshooting

### Editor Not Loading?
- Clear browser cache
- Refresh the page
- Check browser console for errors

### Images Not Uploading?
- Check file size (max 5MB recommended)
- Use supported formats: JPG, PNG, GIF
- Ensure proper permissions on media folder

### Links Not Working?
- Use full URLs for external links: `https://example.com`
- Use relative URLs for internal links: `/about-us`
- For anchors, always use `#anchor-name`

---

## 📞 Need Help?

If you have questions about using the editor:
1. Check this guide first
2. Try the "Source" button to see HTML
3. Test in preview mode before publishing
4. Contact your developer if issues persist

---

**Happy Writing! ✍️**

Your content is now more powerful with rich formatting, anchor tags, and professional styling options!





