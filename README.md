# Junhao Jia — academic homepage

English academic homepage for **Junhao Jia** (`JonahJia`), based on [luost26/academic-homepage](https://github.com/luost26/academic-homepage).

Target address: https://jonahjia.github.io

A responsive profile and publications site with editable Markdown and YAML content. Until individual publication entries are added, the site links to Google Scholar.

## Deploy to GitHub Pages

1. Create a public repository named `JonahJia.github.io` under the `JonahJia` account.
2. Add these project files to its `main` branch, including `.github/workflows/pages.yml`.
3. In **Settings → Pages → Build and deployment → Source**, choose **GitHub Actions**.
4. Run **Actions → Build and deploy academic homepage → Run workflow**, or push a commit.
5. After the workflow succeeds, open https://jonahjia.github.io.

The workflow builds Jekyll using Ruby 3.3. The root-site `baseurl` is already set to an empty string. No custom domain is configured.

## Edit content

| Content | File |
| --- | --- |
| Name, bio, affiliation, education, email, portrait | `_data/profile.yml` |
| Navigation | `_data/navigation.yml` |
| Visible homepage sections | `_data/display.yml` |
| Author highlighting | `_data/authors.yml` |
| Publications | `_publications/` — one Markdown file per paper |
| News | `_news/` — one Markdown file per item |
| Additional styling | `assets/css/profile.css` |

To add a publication, create a Markdown file in `_publications/` with YAML front matter: `title`, `date`, `selected`, `pub`, `pub_date`, `authors`, and `links`. Set `selected: true` to show it on the homepage. An optional `cover` can point to a local figure. The publication page automatically groups entries by year. Until papers are added, it links to the owner’s Google Scholar profile.

To show confirmed education or news later, populate their content and enable `show_experience` or `show_news` in `_data/display.yml`.

## Local preview

Install Ruby and Bundler, then run:

```sh
bundle install
bundle exec jekyll serve
```

Open the address printed by Jekyll. Restart after changing `_config.yml`.

## Credit and license

Adapted from academic-homepage, upstream commit `69f658932b7c912305a861b88a0cadcfac46e071`. Original MIT license retained in `LICENSE`. The footer retains the template link.
