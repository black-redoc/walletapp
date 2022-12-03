const menu_btn = document.getElementById("menu-btn")
const side_nav = [...document.getElementsByClassName("side-nav")][0]
let nav_links = document.getElementsByClassName("nav-show")
nav_links = [...nav_links]


menu_btn.onclick = () => {
    if (window.innerWidth > 1100) {
        side_nav.classList.toggle("w-80px")
        if (nav_links[0].classList.contains("nav-hide")) {
            setTimeout(
                () => {
                    menu_btn.classList.toggle("mt-9px")
                    menu_btn.classList.toggle("mb-9px")
                    nav_links.forEach(
                        element => element.classList.toggle("nav-hide")
                    );
                },
                500
            )
        } else {
            menu_btn.classList.toggle("mt-9px")
            menu_btn.classList.toggle("mb-9px")
            nav_links.forEach(
                element => element.classList.toggle("nav-hide")
            );
        }
    } else {
        side_nav.classList.toggle("w-260px")

        if (!nav_links[0].classList.contains("nav-hide")) {
            setTimeout(
                () => {
                    menu_btn.style.marginTop = "margint-top: 0"
                    menu_btn.style.marginBottom = "margin-bottom: 0"
                    nav_links.forEach(
                        element => element.classList.toggle("nav-hide")
                    );
                },
                500
            )
        } else {
            menu_btn.style.marginTop = "margint-top: 8px"
            menu_btn.style.marginBottom = "margin-bottom: 8px"
            nav_links.forEach(
                element => element.classList.toggle("nav-hide")
            );
        }
    }
}
