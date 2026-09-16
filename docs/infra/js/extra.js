document$.subscribe(({ body }) => {
    renderMathInElement(body, {
        delimiters: [
            { left: "$$", right: "$$", display: true },
            { left: "$", right: "$", display: false },
            { left: "\\(", right: "\\)", display: false },
            { left: "\\[", right: "\\]", display: true },
        ],
        macros: {
            "\\N": "\\mathbb{N}",
            "\\Z": "\\mathbb{Z}",
            "\\Q": "\\mathbb{Q}",
            "\\R": "\\mathbb{R}",
            "\\LN": "\\left.",
            "\\RN": "\\right.",
            "\\LP": "\\left(",
            "\\RP": "\\right)",
            "\\LS": "\\left\\lbrace",
            "\\RS": "\\right\\rbrace",
            "\\LA": "\\left\\langle",
            "\\RA": "\\right\\rangle",
            "\\LB": "\\left[",
            "\\RB": "\\right]",
            "\\MM": "\\ \\middle|\\ ",
            "\\exp": "\\text{exp}",
            "\\abs": "\\left\\vert#1\\right\\vert",
            "\\msr": "m\\left(#1\\right)",
            "\\inv": " #1^{-1}",
            "\\bkt": "\\LA \\img{ #1}\\RA",
        },
    });
});
