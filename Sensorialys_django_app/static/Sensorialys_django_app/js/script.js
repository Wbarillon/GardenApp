/* Script that go to previous page */

function goBack() {
    window.history.back();
}

/* Script that is used in wizard form in order to change color of "buttons" */

const elements = document.querySelectorAll('label');

elements.forEach(
    function(element) {
        console.log(element)
        element.setAttribute('tabindex', '0');
        element.addEventListener('focus', (event) => {
            event.target.classList.toggle('checked');
        });
        element.addEventListener('focusout', (event) => {
            event.target.classList.remove('checked');
        });
    }
)

/* Script that provides a pop-up menu for mobile version */

const opener = document.getElementById("menu-burger");
const closer = document.getElementById("menu-burger-retract");
const menu = document.getElementById("mobile-menu");

opener.setAttribute('tabindex', '0');
closer.setAttribute('tabindex', '0');

opener.addEventListener('click', (event) => {
    menu.style.display = "flex";
});
menu.addEventListener('click', (event) => {
    menu.style.display = "none";
})

/* Script that provides a sticky header */
/*
if (window.location.pathname === '/ressources_jardin') {

    window.onscroll = function() {stickyHeader()};

    let header = document.getElementById('header');
    let listHeader = document.querySelector('.list-header');
    let sticky = header.offsetTop;

    function stickyHeader() {
        if (window.pageYOffset >= sticky) {
            header.classList.add('sticky-header');
            listHeader.classList.add("sticky-listHeader");
        }
        else {
            header.classList.remove("sticky-header");
            listHeader.classList.remove("sticky-listHeader");
        }
    }
}
*/

/*
window.onscroll = function() {stickyHeader(header, search_bar)};

let header = document.getElementById('header');
let sticky = header.offsetTop;

function stickyHeader(element, search_bar) {
  if (window.pageYOffset >= sticky) {
    element.classList.add('sticky')
    search_bar.classList.add('adjusted-search-bar')
  } else {
    element.classList.remove('sticky');
  }
}
*/

/* Script that adds / removes classes on focus / focusout */
/*
const labels = document.querySelectorAll('#actualiser_lot ul li label');
const dates = document.querySelectorAll('#actualiser_lot > li:not(:first-of-type)');

let i;

let tab_dates = [];
let tab_labels = [];

dates.forEach(
    function(date) {
        tab_dates.push(date)
        date.setAttribute('tabindex', '0');
        date.addEventListener('focus', (event) => {
            console.log("focus date")
            date.classList.add('revealed');
        });
    }
)

labels.forEach(
    function(label) {
        label.setAttribute('tabindex', '0');
        if (label.childNodes[0].value == "Récoltable") {

        }
        else {
            tab_labels.push(label.childNodes[0].value)
        }
        label.addEventListener('focus', (event) => {
            for (i = 0; i < tab_dates.length; i++) {
                switch (label.childNodes[0].value) {
                    case tab_labels[i]:
                        console.log("focus label")
                        tab_dates[i].classList.add('revealed');
                }
            }
        });
        label.addEventListener('blur', (event) => {
            for (i = 0; i < tab_dates.length; i++) {
                if (tab_dates[i].classList.contains('revealed')) {
                    console.log("blur if")
                    tab_dates[i].setAttribute('selected', true);
                }
                else {
                    console.log("blur else")
                    tab_dates[i].setAttribute('selected', false);
                }
            }
        });
        label.addEventListener('focusout', (event) => {
            for (i = 0; i < tab_dates.length; i++) {
                console.log("focusout")
                tab_dates[i].classList.remove('revealed');
            }
        });
    }
)
*/
/* Script that adds / removes classes on focus / focusout - V2 */
/*
const labels = document.querySelectorAll('#actualiser_lot ul li label');
const dates = document.querySelectorAll('#actualiser_lot > li:not(:first-of-type)');

let i;

let tab_dates = [];
let tab_labels = [];

dates.forEach(
    function(date) {
        tab_dates.push(date)
        date.setAttribute('tabindex', '0');
        date.setAttribute('class', 'hidden');
        date.addEventListener('focus', (event) => {
            date.setAttribute('selected', true);
            date.classList.remove('hidden');
        });
    }
)

labels.forEach(
    function(label) {
        label.setAttribute('tabindex', '0');
        if (label.childNodes[0].value == "Récoltable") {

        }
        else {
            tab_labels.push(label.childNodes[0].value)
        }
        label.addEventListener('focus', (event) => {
            for (i = 0; i < tab_dates.length; i++) {
                switch (label.childNodes[0].value) {
                    case tab_labels[i]:
                        tab_dates[i].classList.remove('hidden');
                }
            }
        });
        label.addEventListener('blur', (event) => {
            for (i = 0; i < tab_dates.length; i++) {
                if (tab_dates[i].classList.contains('hidden')) {
                    tab_dates[i].setAttribute('selected', false);
                }
                else {
                    tab_dates[i].setAttribute('selected', true);
                }
            }
        });
        label.addEventListener('focusout', (event) => {
            for (i = 0; i < tab_dates.length; i++) {
                tab_dates[i].classList.add('hidden');
            }
        });
    }
)*/