use dioxus::prelude::*;

const CSS: Asset = asset!("/assets/main.css");
#[derive(Clone, PartialEq)]
pub struct Distro {
    id: usize,
    name: String,
    description: String,
    image: String,
}
#[component]
fn app() -> Element {
    rsx! {
        document::Stylesheet { href: CSS }
        div { id: "title",
            h1 { "Distroshop" }
        }
        DistroList {}
    }
}

#[component]
fn DistroList() -> Element {
    // the following structs are to be downloaded in the background from a raw github json file (of my own making) and parsed into structs
    let mint = Distro {
        id: 1,
        name: String::from("linux mint"),
        description: String::from("test"),
        image: String::from("https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fseeklogo.com%2Fimages%2FL%2Flinux-mint-logo-49124587FE-seeklogo.com.png&f=1&nofb=1&ipt=006bd30080a4f66f36a6084bd905a9ab37c9bab338eb0f3565936edc3ae49c0f"),
    };
    let ubuntu = Distro {
        id: 2,
        name: String::from("ubuntu"),
        description: String::from("test"),
        image: String::from("https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fbrandslogos.com%2Fwp-content%2Fuploads%2Fimages%2Flarge%2Fubuntu-logo.png&f=1&nofb=1&ipt=adcd2a61bd1d5cc0143846354fc74db0629d6eec21f9c688641eb9df72e222fc"),
    };

    let fedora = Distro {
        id: 3,
        name: String::from("fedora"),
        description: String::from("test"),
        image: String::from("https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Flogodix.com%2Flogo%2F536504.png&f=1&nofb=1&ipt=82721ca3ed8ba6ff8fc89d04e85252c1721dfe83762cf7b08763bff5fe25ba2c"),
    };

    let arch = Distro {
        id: 4,
        name: String::from("arch linux"),
        description: String::from("test"),
        image: String::from("https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fw7.pngwing.com%2Fpngs%2F368%2F108%2Fpng-transparent-arch-linux-linux-distribution-installation-xfce-linux-text-triangle-logo-thumbnail.png&f=1&nofb=1&ipt=12a88c98960f7fc6530750746672af3848e6e3e310f7059711f9986f26a48105"),
    };
    let distros = vec![mint, ubuntu, fedora, arch];
    rsx! {
        div {
            id: ("distrolist"),
            style: ("display: grid; grid-template-columns: repeat(2,1fr); gap: 12px; list-style-type: none; padding:0;"),
            for distro in distros {
                li { style: "border: 3px solid #7a7a7a;",
                    img {
                        style: "max-width:100px; max-height:100px; width: auto; height:auto;",
                        src: ({ distro.image }),
                    }
                    h3 { "{distro.name}" }
                    p { "{distro.description}" }
                    button { "Download and Flash" } //will use dd and tokio
                }
            }
        }
    }
}

fn main() {
    dioxus::launch(app);
}
