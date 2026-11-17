# Junhao Jia — academic homepage

English academic homepage for **Junhao Jia** (`JonahJia`), based on [luost26/academic-homepage](https://github.com/luost26/academic-homepage).

Live site: https://jonahjia.github.io/

## Content and appearance

| Content | File |
| --- | --- |
| Bio, contact details, education, experience, honors, service | `_data/homepage.yml` |
| Institution logos | `_data/institutions.yml` |
| All publication metadata, ordered full authors, verified links and framework images | `_data/papers.yml` |
| Author highlighting and personal homepage links | `_data/paper_authors.yml` |
| Dated conference news | `_data/updates.yml` |
| Navigation | `_data/navigation.yml` |
| Homepage and legacy publications URL redirect | `index.html`, `publications.html` |
| Reusable page sections | `_includes/academic/` |
| Styling and framework image enlargement | `assets/css/academic.css`, `assets/js/academic.js` |

The data files use JSON syntax, which is valid YAML and is read by Jekyll. Education and research experience precede news and publications. Three selected first-author papers use image cards; the other four publications use compact entries. Each framework image opens at a larger size. Full author lists are retained, with Junhao Jia highlighted in Tsinghua purple (`#660874`) and equal contributions marked with `*`.

The site uses a single-page layout: Home jumps to the top, and Publications jumps to the homepage’s publications section. The old `/publications.html` URL redirects to `/#publications`. Publication resource buttons are currently hidden; their link metadata is retained for later use.

The homepage currently ends with publications. Honors, open source, and academic service remain in the source and can be restored by setting `show_additional_sections: true` in the front matter of `index.html`.

Keep news entries in descending `YYYY.MM` order, link to the conference homepage, and put acceptance, oral selection and award selection in separate entries. Assets and source credits are in `assets/images/logos/` and `assets/images/publications/`. Older template data and widgets remain available but are not used by the new homepage.

## GitHub Pages deployment

The `main` branch is deployed by `.github/workflows/pages.yml` using Ruby 3.3 and Jekyll. GitHub Pages is configured to use GitHub Actions. Each push to `main` rebuilds and deploys the site. The root-site `baseurl` is empty; no custom domain is configured.

## Local development

Install Ruby and Bundler, then run:

```sh
bundle install
bundle exec jekyll serve
```

For a production build, use `bundle exec jekyll build`. Restart Jekyll after changes to `_config.yml`.

## Credits and licenses

Adapted from academic-homepage, upstream commit `69f658932b7c912305a861b88a0cadcfac46e071`. The original MIT license is retained in `LICENSE`, and the footer links to the template. Institution logos and original paper figures have separate provenance notes beside their files. The Tsinghua vector asset includes its upstream GPL-3.0 license.
