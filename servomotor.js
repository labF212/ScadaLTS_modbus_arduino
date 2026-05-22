//servo motor
var angulo = Math.max(45, Math.min(135, value));
var cor = "#2ecc71";

if (angulo < 60) {
    cor = "#ff4d4d";
} else if (angulo > 130) {
    cor = "#ffcc00";
}

var largura = ((angulo - 45) / 90) * 100;

// Criando o HTML em partes dentro de um Array sem quebras de texto inválidas
var html = [
    "<div style='width:320px; height:300px; padding:15px; border-radius:20px; background:#f2f2f2; border:2px solid #cccccc; font-family:Arial; box-shadow:0px 4px 10px rgba(0,0,0,0.2); box-sizing:border-box;'>",
    "<div style='font-size:22px; font-weight:bold; text-align:center; margin-bottom:15px; color:#333;'>Servo Motor</div>",
    "<div style='background:white; border-radius:15px; padding:15px; text-align:center; box-shadow:0 2px 6px rgba(0,0,0,0.1); height:200px;'>",
    "<div style='font-size:16px; color:#555; margin-top:8px;'>⚙️ Ângulo do Servo</div>",
    "<div style='margin-top:25px; font-size:38px; font-weight:bold; color:#222;'>",
    angulo.toFixed(0),
    "°</div>",
    "<div style='margin-top:25px; height:18px; width:100%; background:#ddd; border-radius:10px; overflow:hidden;'>",
    "<div style='height:100%; width:",
    largura,
    "%; background:",
    cor,
    ";'></div>",
    "</div>",
    "<div style='display:flex; justify-content:space-between; font-size:11px; margin-top:6px; color:#666;'>",
    "<span>45°</span><span>90°</span><span>135°</span>",
    "</div>",
    "</div>",
    "</div>"
];

// O .join('') junta todos os pedaços do array em uma única string sem usar o "+"
return html.join('');