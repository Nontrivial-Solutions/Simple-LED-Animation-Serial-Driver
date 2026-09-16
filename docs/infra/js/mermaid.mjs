import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11.16.0/dist/mermaid.esm.min.mjs";

mermaid.registerIconPacks([
    {
        name: "logos",
        loader: () => import("@iconify-json/logos").then((module) => module.icons),
    },
    {
        name: "material-icon-theme",
        loader: () => import("@iconify-json/material-icon-theme").then((module) => module.icons),
    },
    {
        name: "line-md",
        loader: () => import("@iconify-json/line-md").then((module) => module.icons),
    },
    {
        name: "carbon",
        loader: () => import("@iconify-json/carbon").then((module) => module.icons),
    },
    {
        name: "material-symbols",
        loader: () => import("@iconify-json/material-symbols").then((module) => module.icons),
    },
    {
        name: "mdi",
        loader: () => import("@iconify-json/mdi").then((module) => module.icons),
    },
]);

mermaid.initialize({
    startOnLoad: false,
    securityLevel: "loose",
});

// Important: necessary to make it visible to Material for MkDocs
window.mermaid = mermaid;
