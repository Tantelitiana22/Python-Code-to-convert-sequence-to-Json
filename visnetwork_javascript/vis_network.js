
let slider = document.getElementById("myRange");
let output = document.getElementById("demo");
output.innerHTML = slider.value;
let valueFilter = slider.value;

slider.oninput = function() {
    output.innerHTML = this.value;
    valueFilter=this.value;
    draw();
};

function isNext(currentNode,edge){
    for(let i=0;i<edge.length;i++){
        if(edge[i]["from"]===currentNode){
            return true;
        }
    }
    return false;
}
function isLast(currentNode,edge){
    for(let i=0;i<edge.length;i++){
        if(edge[i]["to"]===currentNode){
            return true;
        }
    }
    return false;
}

function dataTransform(dataJson,valueFilter){
    console.log(typeof valueFilter)
    let  vertex = [];
    let  edges = [];
    let imageFile ="";

    for(let i=0;i<dataJson.edges.length;i++){
        let edge = dataJson.edges[i];

        if(edge["size"]>=parseFloat(valueFilter)){
            edges.push({from:edge["from"],to:edge["to"],label:edge["size"].toString()});
        }
    }

    for(let i=0;i<dataJson.nodes.length;i++){

        let node = dataJson.nodes[i]["node"];
        let size = dataJson.nodes[i]["size"];
        let canal = node.split(":")[0];
        switch (canal) {
            case "magasin":
                imageFile = "ImageData/magasin.jpg";
                break;
            case "kiosque":
                imageFile = "ImageData/kiosque.jpg";
                break;
            case "mail":
                imageFile = "ImageData/mail.jpg";
                break;
            case "mobile":
                imageFile = "ImageData/mobile.jpg";
                break;
            default:
                imageFile = "ImageData/web.jpg";
        }

        if(isNext(node,edges) || isLast(node,edges)){
            vertex.push({id:node,image:imageFile,label:node,size:size/12,shape:"image"});
        }
    }


    return {"nodes":vertex,"edges":edges};
}
// Called when the Visualization API is loaded.
function draw() {
    // create people.
    let container = document.getElementById('mynetwork');

    let options = {

        width: '1600px',
        height: '800px',
        nodes: {
            color: {
                background: '#006400'
            },
            font: {color: '#0A0A0A', "size": 10},
        },
        edges: {
            style: 'curve',
            type:"vee",
            arrows:"from"

        },


    };

    let json = $.getJSON("MarkovResult.json")
        .done(function(dataJson){

            let result =  dataTransform(dataJson,valueFilter);
            let data = {
                nodes: result.nodes,
                edges: result.edges
            };
            let network = new vis.Network(container, data, options);
        });

}