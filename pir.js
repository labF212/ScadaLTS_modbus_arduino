// PIR

var estado = (value == 1);
var cor = estado ? "green" : "red";

var html = [
    "<div style='width:320px; height:300px; padding:15px; border-radius:20px; background:#f2f2f2; border:2px solid #cccccc; font-family:Arial; box-shadow:0px 4px 10px rgba(0,0,0,0.2); box-sizing:border-box;'>",

    // Título
    "<div style='font-size:22px; font-weight:bold; text-align:center; margin-bottom:15px; color:#333;'>PIR</div>",

    // Caixa branca (subtítulo + LED)
    "<div style='background:white; border-radius:15px; padding:15px; text-align:center; box-shadow:0 2px 6px rgba(0,0,0,0.1); height:200px; display:flex; flex-direction:column; justify-content:center; align-items:center;'>",

        // Subtítulo
        "<div style='font-size:16px; color:#555; margin-bottom:20px; display:flex; align-items:center; gap:8px;'>",
        "👁️‍🗨️ Estado do PIR",
        "</div>",

        // LED
        "<div style='width:80px; height:80px; border-radius:50%; background:",
        cor,
        "; box-shadow:0 0 25px ",
        cor,
        ";'></div>",

    "</div>",

    "</div>"
];

return html.join('');