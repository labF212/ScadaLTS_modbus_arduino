//grafico LDR

// Criando o HTML em partes dentro de um Array
var html = [
    "<div style='width:600px; height:500px; padding:15px; border-radius:20px; background:#f2f2f2; border:2px solid #cccccc; font-family:Arial; box-shadow:0px 4px 10px rgba(0,0,0,0.2); box-sizing:border-box;'>",
    "<div style='font-size:22px; font-weight:bold; text-align:center; margin-bottom:15px; color:#333;'>LDR</div>",
    // Retângulo branco expandido (height: 410px) e alinhado ao topo (flex-start)
    "<div style='background:white; border-radius:15px; padding:20px; text-align:center; box-shadow:0 2px 6px rgba(0,0,0,0.1); height:410px; display:flex; flex-direction:column; justify-content:flex-start; align-items:center; box-sizing:border-box;'>",
    // Uma única div unindo o texto e o valor na mesma linha, mesma fonte e cor
    "<div style='font-size:24px; font-weight:bold; color:#333; margin-top:10px;'>☀️ Luminosidade atual: ",
    value.toFixed(0),
    "</div>",
    "</div>", // Fecha a div do fundo branco
    "</div>"  // Fecha a div principal do container
];

// O .join('') junta todos os pedaços do array em uma única string sem usar o "+"
return html.join('');

//DP_129771