//motor dc
// Correção: Garante que o valor fique travado corretamente entre 0 e 254
var valor_permitido = Math.max(0, Math.min(254, value));

// Criando o HTML em partes dentro de um Array
var html = [
    "<div style='width:320px; height:350px; padding:15px; border-radius:20px; background:#f2f2f2; border:2px solid #cccccc; font-family:Arial; box-shadow:0px 4px 10px rgba(0,0,0,0.2); box-sizing:border-box;'>",
    "<div style='font-size:22px; font-weight:bold; text-align:center; margin-bottom:15px; color:#333;'>Motor DC</div>",
    "<div style='background:white; border-radius:15px; padding:15px; text-align:center; box-shadow:0 2px 6px rgba(0,0,0,0.1); height:250px;'>",
    "<div style='font-size:16px; color:#555; margin-top:8px;'>🚁 Velocidade do Motor</div>",
    "<div style='margin-top:150px; font-size:38px; font-weight:bold; color:#222;'>",
    valor_permitido.toFixed(0),
    " PWM</div>",
    "</div>", // Fecha a div do fundo branco
    "</div>"  // Fecha a div principal do container (a tag extra que estava aqui foi removida)
];

// O .join('') junta todos os pedaços do array em uma única string sem usar o "+"
return html.join('');