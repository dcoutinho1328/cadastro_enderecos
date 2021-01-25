function botao_passar(elemento){
    elemento.style.fontWeight="bolder";
    elemento.style.backgroundColor="rgb(255, 255, 255)";
    elemento.style.color=" rgb(90, 90, 90)"
}

function botao_sair(elemento){
    elemento.style.fontWeight="normal";
    elemento.style.backgroundColor="rgb(90, 90, 90)";
    elemento.style.color=" rgb(255, 255, 255)"
}

function MascaraCep(cep){
    if(mascaraInteiro(cep)==false){
    event.returnValue = false;
}       
return formataCampo(cep, '00.000-000', event);
}