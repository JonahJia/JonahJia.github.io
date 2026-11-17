# Sidebar design source

The official homepage at `/` adapts the MIT-licensed design from [Yifei Sun's homepage](https://diaoquesang.github.io/) and [diaoquesang/diaoquesang.github.io](https://github.com/diaoquesang/diaoquesang.github.io), inspected at commit `4a5aaf80e805fdc7812187f066589365824eaf3f` on 17 November 2026. The upstream MIT license (Copyright 2022 Yi Ren) is preserved in `LICENSE-REFERENCE`.

`assets/css/sidebar-reference.css` retains the reference site's visual system without the music player. `sidebar-personal.css` preserves Junhao Jia's author color, complete framework figures and vertically centered publication text. Compact publication entries alternate white and light gray backgrounds. `assets/js/sidebar.js` provides navigation, theme switching, overflow hints, accessible drawer states and the framework image viewer.

`index.html` uses the sidebar layout and all confirmed profile and research sections, including eight conference papers and two illustrated preprints. The supplied portrait and the owner's confirmed honors, funding, services, patents, software, competitions and open source projects are included. Source notes for figures and logos are stored alongside their assets; the two requested software demonstration GIFs are embedded from the coauthor's site.

`design-preview.html` redirects the former `/preview/` URL to the official homepage, preserving section anchors. The legacy `/publications.html` URL redirects to `/#publications`. The homepage has a root canonical URL and portrait sharing metadata, without a preview title or noindex directive.

The profile badges use the owner's Scholar ID and a separate visitor counter for https://jonahjia.github.io. The Pages workflow refreshes Scholar citations daily; unavailable data keeps the last verified count, and an initial unknown value is displayed as a dash.
