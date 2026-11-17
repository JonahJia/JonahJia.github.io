# Sidebar design source

The sidebar layout preview at `/preview/` adapts the MIT-licensed design from [Yifei Sun's homepage](https://diaoquesang.github.io/) and [diaoquesang/diaoquesang.github.io](https://github.com/diaoquesang/diaoquesang.github.io), inspected at commit `4a5aaf80e805fdc7812187f066589365824eaf3f` on 17 November 2026.

The upstream MIT license (Copyright 2022 Yi Ren) is preserved in `LICENSE-REFERENCE`.

`assets/css/sidebar-reference.css` retains the reference site's visual system, without the music player. `sidebar-personal.css` preserves Junhao Jia's selected author color, complete paper figures, vertically centered publication text, and uniform compact publication backgrounds. `assets/js/sidebar.js` adapts the reference navigation, theme switch, and overflow hints, adding accessible drawer states and the existing figure viewer.

The preview uses the previously confirmed profile, institutions, mentors, news and seven papers. No reference-owner biography, personal social accounts, verification tokens, analytics, music, memberships, grants or patents have been copied. Honors and services remain hidden in accordance with the latest confirmed content scope. Software markup is prepared but is not rendered until the owner's entries have been confirmed and supplied in `_data/software.yml`.

The current homepage remains at `/`; `design-preview.html` is a noindex design preview. To adopt it after content review, use its sidebar layout and content for `index.html`, retaining the existing legacy `/publications.html` redirect to the homepage's publications section.
