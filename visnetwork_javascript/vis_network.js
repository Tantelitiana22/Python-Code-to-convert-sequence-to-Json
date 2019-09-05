function dataTransform(dataJson){
    let  vertex = [];
    let  edges = [];
    let imageFile ="";
    console.log(dataJson);
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

        vertex.push({id:node,image:imageFile,label:node,size:size/12,shape:"image"})
    }

    for(let i=0;i<dataJson.edges.length;i++){
        let edge = dataJson.edges[i];
        edges.push({from:edge["from"],to:edge["to"],label:edge["size"].toString()})
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
            let result =  dataTransform(dataJson);
            let data = {
                nodes: result.nodes,
                edges: result.edges
            };
            let network = new vis.Network(container, data, options);
        });

}