/* Errance Bar - Double height in small windows */

var window_width_trigger = 1200;
var errance_bar_trigger = document.getElementById("errance-bar-trigger");
var errance_bar = document.getElementById("errance-bar");

errance_bar_trigger.addEventListener("click", function(e) {
    e.preventDefault();
    if (errance_bar.classList.contains("expanded")) { 
        errance_bar.classList.remove("expanded");
    } else {
        errance_bar.classList.add("expanded");
    }

    if (window.innerWidth < window_width_trigger) {
        errance_bar.setAttribute("expanded_size", "double");
    } else {
        errance_bar.setAttribute("expanded_size", "simple");
    }
});

window.addEventListener("resize", function(e) {
    if (window.innerWidth < window_width_trigger) {
        errance_bar.setAttribute("expanded_size", "double");
    } else {
        errance_bar.setAttribute("expanded_size", "simple");
    }
});


/* Media Bar - Highlight selectec media type */

var media_bar = document.getElementById("media-bar");
if (media_bar) {
    var hrefs = window.location.href.split('/');
    var mtype = hrefs[hrefs.length - 1];
    if (!isNaN(parseInt(mtype.charAt(0)))) {
        mtype = hrefs[hrefs.length - 2];
    }
    links = media_bar.getElementsByTagName("li");
    for (var i=0; i<links.length; i++) {
        link = links[i].getElementsByTagName("a")[0]
        if (link.getAttribute("desc") == mtype) {
            link.classList.add("selected");
        }
    }
}


/* Collection - Display oeuvres by chunks */
var txt_decoder = document.createElement("textarea");
function decodeHtml(html) {
    txt_decoder.innerHTML = html;
    return txt_decoder.value;
}

var chunk_size = 25;
var collection = document.getElementById("collection");
if (collection) {
    console.log(oeuvres);
    for (i=0; i<oeuvres.length/chunk_size; i++) {
        var ul = document.createElement("ul");
        ul.classList.add("collection_chunk");
        collection.appendChild(ul);
        for (j=0; j<chunk_size; j++) {
            if (oeuvres[chunk_size*i+j]) {
                var a = document.createElement("a");
                var text = decodeHtml(oeuvres[chunk_size*i+j][0]);
                var textNode = document.createTextNode(text);
                a.href = oeuvres[chunk_size*i+j][1];
                a.appendChild(textNode);
                var li = document.createElement("li");
                li.appendChild(a);
                ul.appendChild(li);
            }
        }
    }
}

