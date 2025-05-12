# Academic Website - Juan Felipe Imbet

This repository contains the source code for my academic website, hosted via GitHub Pages.

## Website Structure

- **index.html**: Main landing page with research papers and publications
- **teaching**: Folder containing teaching-related materials and pages
- **assets**: Contains all static resources
  - **css**: Custom stylesheets
  - **js**: JavaScript files
  - **images**: Images for the website

## Features

- Responsive design using Bootstrap 5
- Clean, accessible presentation of research papers
- Collapsible abstracts and media mentions with toggle buttons
- Organized teaching materials 
- Mobile-friendly layout
- Easy to maintain with static HTML content

## Development

### Updating the Website

#### Adding a New Paper

To add a new research paper to your website:

1. Open `index.html`
2. Navigate to the "Working Papers" section
3. Copy an existing paper card and update the following:
   - Paper title and link
   - Publication status
   - Authors (make sure your name is in `<strong>` tags)
   - Abstract
   - Media mentions (if applicable)

Example template for a new paper:

```html
<div class="col-md-12 mb-4">
    <div class="card paper-card">
        <div class="card-body">
            <h3 class="card-title paper-title">
                <a href="[PAPER_URL]" target="_blank">
                    [PAPER_TITLE]
                </a>
            </h3>
            <p class="paper-status">[PUBLICATION_STATUS]</p>
            <p class="paper-authors">[AUTHOR1], <strong>Juan Felipe Imbet</strong>, [AUTHOR3]</p>
            <div class="paper-abstract collapse">
                <p class="mt-3"><strong>Abstract:</strong> [PAPER_ABSTRACT]</p>
            </div>
            <button class="btn btn-sm btn-outline-primary mt-2 toggle-abstract">Show Abstract</button>
            
            <!-- Add media mentions if applicable -->
            <div class="media-mentions mt-3 collapse">
                <h5><i class="fas fa-newspaper me-2"></i>Media Mentions</h5>
                <ul>
                    <li><a href="[MENTION_URL]" target="_blank">[MENTION_TITLE]</a></li>
                    <!-- Add more media mentions as needed -->
                </ul>
            </div>
            <button class="btn btn-sm btn-outline-secondary mt-2 toggle-mentions">Show Media Mentions</button>
        </div>
    </div>
</div>
```

#### Adding a Publication

To add a new publication to your website:

1. Open `index.html`
2. Navigate to the "Publications" section
3. Copy an existing publication card and update the following:
   - Publication title
   - Journal name and status
   - Authors (make sure your name is in `<strong>` tags)

Example template for a new publication:

```html
<div class="col-md-12">
    <div class="card mb-4 paper-card">
        <div class="card-body">
            <h3 class="card-title paper-title">[PUBLICATION_TITLE]</h3>
            <p class="paper-status">[JOURNAL_NAME]</p>
            <p class="paper-authors">[AUTHOR1], <strong>Juan Felipe Imbet</strong>, [AUTHOR3]</p>
        </div>
    </div>
</div>
```

#### Updating Your CV

To update your CV:

1. Replace the `cv.pdf` file with your updated CV
2. Make sure the filename remains `cv.pdf` to maintain all links

### Updating Teaching Materials

Place your teaching materials in the appropriate subfolder under `teaching/` and update the corresponding index page.

## Deployment

The website is deployed automatically via GitHub Pages whenever changes are pushed to the main branch.

## License

All rights reserved. © Juan Felipe Imbet