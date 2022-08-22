function showChoosingPanel(document, question, ca_func, answerSheet, multiple, images, media_url){
    var stem = document.createElement('p');
    stem.id = question.id;
    stem.name = "choosing-stem";
    stem.innerHTML = parseInt(i) + 1;
    stem.innerHTML += "." + question.stem;
    document.body.appendChild(stem);
    for(j in images){
        var box = document.createElement('div');
        var img_name = document.createElement('p');
        img_name.innerHTML = images[j];

        var img = document.createElement('img');
        img.src = media_url + images[j];
        img.height = "250";
        img.style.display = "block";
        img.style.cssText += "box-shadow: 0px 0px 4px #555";
        box.appendChild(img);
        box.appendChild(img_name);
        img_name.style.cssText = "opacity: 0.5"
        document.body.appendChild(box);
    }
    for(i in question.choices){
        (function(i)
        {
            var ele = document.createElement("button");
            document.body.appendChild(ele);
            ele.id = question.choices[i].id;
            ele.name = question.id + "-choice";
            ele.style = "background: #CCC; border: gray solid 1px; border-radius: 2px; width: 80%; height: 32px";
            ele.onclick = function (){
                ca_func(question, ele.id, answerSheet, multiple);
            }
            ele.innerHTML = question.choices[i].content;

        })(i);
    }
}


function showFillingPanel(document, question){
    var stem = document.createElement('p');
    stem.id = question.id;
    stem.name = "filling-stem";
    stem.font = "Arial";
    stem.innerHTML = parseInt(i) + 1;
    stem.innerHTML += "." + question.stem;
    document.body.appendChild(stem);
    var textbox = document.createElement("textarea");
    textbox.id = "comp-" + question.id;
    textbox.style.width = "79%";
    textbox.style.height = "40px"
    document.body.appendChild(textbox);
}

function ajaxGet(url, xml){
    xml.open("GET", url, true);
    xml.send();
}

function click(id){
    if(document.all){
        document.getElementById(id).click();
    }else{
        var event = document.createEvent("MouseEvents");
        event.initEvent("click", true, true);
        document.getElementById(id).dispatchEvent(event);
    }
}

function sleep(time){
    for(var t = Date.now(); Date.now() - t <= time;);
}

function refactor(event, folder_id, url, last){
    console.log(folder_id);
    var last_id = event.dataTransfer.getData("last_folder");
    console.log(last_id);
    if(folder_id!=last_id){
        var draggedId = event.dataTransfer.getData("book");
        var xml = new XMLHttpRequest();
        xml.onreadystatechange = function(){
            if(xml.readyState == 4 && xml.status == 200){
                location.reload();
            }
        }
        var data = {
            "folder": folder_id,
            "book": draggedId
        }
        xml.open("POST", url, true);
        xml.setRequestHeader('Content-type','application/x-www-form-urlencoded');
        xml.send(JSON.stringify(data));
        console.log(JSON.stringify(data));
    }
}


function set_display(card_id, display){
    var target = document.getElementById(card_id);
    if(display){
        target.style.display = "block";
    }else{
        target.style.display = "none";
    }

}


function go_to_mouse(ev, id){
    var eve = window.event || ev;
    var target = document.getElementById(id);
    target.style.left = (eve.pageX + 10) + "px";
    target.style.top = (eve.pageY + 10) + "px";
}
