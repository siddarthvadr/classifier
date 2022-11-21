Dropzone.autoDiscover = false;

function init() {
    let dz = new Dropzone("#dropzone", {
        url: "/",
        maxFiles: 1,
        addRemoveLinks: true,
        dictDefaultMessage: "Some Message",
        autoProcessQueue: false
    });

    dz.on("addedfile", function() {
        if (dz.files[1]!=null) {
            dz.removeFile(dz.files[0]);
        }
    });

    dz.on("complete", function (file) {
        let imageData = file.dataURL;

        var url = "http://127.0.0.1:5000/classify_image";

        $.post(url, {
            image_data: file.dataURL
        },function(data, status) {
           
            console.log(data);
            if (!data || data.length==0) {
                $("#resultHolder").hide();
                $("#divClassTable").hide();
                $("#error").show();
                return;
            }
            let players = ["aayushi", "abhishek", "binod", "vandana", "sid"];

            if(data.length == 2){
                debugger;
                let match1 = null;
                let match2 = null;

                let bestScore1 = -1;
                let bestScore2 = -1;

                let maxScoreForThisClass1 = Math.max(...data[0].class_probability);
                let maxScoreForThisClass2 = Math.max(...data[1].class_probability);

                if(maxScoreForThisClass1>bestScore1) {
                    match1 = data[0];
                    bestScore1 = maxScoreForThisClass1;
                }

                if(maxScoreForThisClass2>bestScore2) {
                    match2 = data[1];
                    bestScore1 = maxScoreForThisClass2;
                }

                

                $("#error").hide();
                $('#divperson-2').show();
                $("#error1").hide();
                $("#resultHolder1").show();
                $("#resultHolder2").show();
                $("#divClassTable1").show();
                $("#divClassTable2").show();
                $("#resultHolder1").html($(`[data-player="${match1.class}"`).html());
                let classDictionary1 = match1.class_dictionary;
                for(let personName in classDictionary1) {
                    let index = classDictionary1[personName];
                    let proabilityScore = match1.class_probability[index];
                    let elementName = "#score0_" + personName;
                    $(elementName).html(proabilityScore);
                }
                $("#resultHolder2").html($(`[data-player="${match2.class}"`).html());
                let classDictionary2 = match2.class_dictionary;
                for(let personName in classDictionary2) {
                    let index = classDictionary2[personName];
                    let proabilityScore = match2.class_probability[index];
                    let elementName = "#score1_" + personName;
                    $(elementName).html(proabilityScore);
                }
            } 
            else{

            let match = null;
            let bestScore = -1;
            for (let i=0;i<data.length;++i) {
                let maxScoreForThisClass = Math.max(...data[i].class_probability);
                if(maxScoreForThisClass>bestScore) {
                    match = data[i];
                    bestScore = maxScoreForThisClass;
                }
            }
            if (match) {
                $("#error").hide();
                $("#resultHolder").show();
                $("#divClassTable").show();
                $("#resultHolder").html($(`[data-player="${match.class}"`).html());
                let classDictionary = match.class_dictionary;
                for(let personName in classDictionary) {
                    let index = classDictionary[personName];
                    let proabilityScore = match.class_probability[index];
                    let elementName = "#score_" + personName;
                    $(elementName).html(proabilityScore);
                }
            }
            // dz.removeFile(file);
        }
        });
    });

    $("#submitBtn").on('click', function (e) {
        dz.processQueue();
    });
}

$(document).ready(function() {
    console.log( "ready!" );
    $("#error").hide();
    $("#resultHolder").hide();
    $("#divClassTable").hide();
    $('#divperson-2').hide();

    init();
});