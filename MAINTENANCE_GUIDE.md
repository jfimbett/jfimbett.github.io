# Website Maintenance Guide

## Summary of Changes

We've made the following improvements to your academic website:

1. **Simplified Structure**: 
   - Removed SSRN scraping scripts and dynamic paper loading
   - Converted to a static HTML approach for easier maintenance
   - Cleaned up unnecessary files and duplicates

2. **Content Updates**:
   - Added all papers directly to index.html with proper formatting
   - Enhanced publication section with abstract
   - Improved organization of teaching materials

3. **Maintenance Improvements**:
   - Added comprehensive README with update instructions
   - Created .gitignore file for cleaner repository
   - Removed dependencies on external data sources

## How to Maintain Your Website

### Updating Research Papers

To update your research papers:

1. Open `index.html`
2. Navigate to the "Working Papers" section
3. Edit the existing paper cards or add new ones following the template in README.md
4. For each paper, you can update:
   - Title and URL
   - Publication status
   - Authors
   - Abstract
   - Media mentions

### Updating Publications

Follow similar steps for the publications section, updating or adding new publications as needed.

### Updating Teaching Materials

Teaching materials are organized in directories:
- `/teaching/python_m1/`
- `/teaching/python_m2/`
- `/teaching/vba_python/`
- `/teaching/empirical_asset_pricing/`
- `/teaching/investment_funds_risks/`

Add new materials to the appropriate directory and update the corresponding index.html file.

### Updating Your CV

Simply replace the `cv.pdf` file with your updated CV, keeping the same filename.

## Best Practices

1. **Make Regular Backups**: Before making major changes, create a backup copy of your files
2. **Test Locally**: View changes locally before pushing to GitHub
3. **Validate HTML**: Use an online validator like validator.w3.org to check your HTML
4. **Optimize Images**: Compress images before adding them to the website
5. **Check Mobile View**: Test your website on mobile devices or using browser development tools

## Need Help?

For future changes or improvements to your website, you can:
1. Refer to this guide and the README.md
2. Use GitHub Copilot or another AI assistant for code suggestions
3. Consider hiring a web developer for major redesigns
