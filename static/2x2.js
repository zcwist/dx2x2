$(document).ready(function(){
    // $(".skill").draggable();
    // $(".skill").click(function(){
    //     console.log("hello world")
    // })
    
    $("#canvasgrid").height(function(){
        return 0.75*$(document).height();
    })
    $("#skills").height(function(){
        return 0.75*$(document).height();
    })
    
    // $("#myCanvas").height($("#canvasgrid").height());
    $.getJSON("/skills/1",function(result){
        skills = result;
        $.each(result,function(i, field){
            $('.skills').append('<div class="row skill" id="'+field.id+'">'+
            field.skill_name +
            "</div>")
        });
        
        $(".skill").draggable({
            helper: function(event){
                var ret = $(this).clone();
                ret.appendTo("#dxcanvas")
                $(this).toggleClass("ghost");
                return ret;
            },
            stop: function(event, ui){
                position = ui.helper.position()
                if (position.left >0){
                    $(this).draggable( "disable" );
                }
                else {
                    $(this).toggleClass("ghost");
                    
                }
            },
            // containment: ["parent",$("#canvasgrid
            containment: $("#mainpanel"),
            revert: false,
        });
        $(".skill").click(function () {
            console.log(this)
        })
    })
    $("#dxcanvas").droppable({
        drop:function(event,ui){
            if (ui.draggable.hasClass('skill')){
                var dropped = ui.draggable.clone();
                $(dropped).toggleClass("ghost");
                $(dropped).removeClass("skill");
                $(dropped).addClass("skill_in_canvas");
                $(dropped).detach().css({'position':'absolute', 'top':ui.position.top,'left':ui.position.left}).appendTo($(this));
                $(dropped).draggable({
                    containment: "parent"
                    });
                // console.log("<div style='float:right' id='"+$(this).attr(id)+"'><sup>&nbsp x</s</div>");
                
                // $(dropped).prepend("<div style='float:right' class='cl' id='"+$(dropped).attr("id")+"'><sup>&nbsp x</s</div>")

                // $(".cl#"+$(dropped).attr("id")).click(function(){
                //     skill_id = $(this).attr("id");
                //     console.log("close"+skill_id);
                //     $(".skill#"+skill_id).toggleClass("ghost");
                //     $(this).parent().remove();
                // })
                
                $(dropped).dblclick(function(){
                    // console.log($(this).attr("id"));
                    
                    skill_id = $(this).attr("id")
                    console.log($(".skill#"+skill_id));
                    $(".skill#"+skill_id).toggleClass("ghost");
                    $(".skill#"+skill_id).draggable("enable");
                    this.remove();
                })
                
                
                
            }
            
        }
    })
    // add the sign out function
    $('#exit').attr('href', '/login');
    //end modificaition
    
    $("#save").click(function(){
        dict = {}
        survey_id = $("#survey_id");
        
        $(".skill_in_canvas").each(function(index){
            console.log($(this).attr("id"));
            console.log($(this).position());
            dict[$(this).attr("id")] = $(this).position();
            //normalize coordinates
        })
        
        $.ajax({
              type:"POST",
              url: "/kaiyue/test",
              data: JSON.stringify({"total":dict}),
              // data: {"total":dict},
              dataType: "json",
              contentType: 'application/json;charset=UTF-8',


              success: function(){
                console.log("data sent");
              }

            })
    })
    var canvas = $("#myCanvas");
    width = canvas.parent().width();
    height = canvas.parent().height();
    console.log(height);
    var canvas = document.getElementById("myCanvas");
    canvas.width = width;
    canvas.height = height;
    var ctx = canvas.getContext("2d");
    ctx.lineWidth=2;
    ctx.moveTo(0.05*width,height/2);
    ctx.lineTo(0.95*width,height/2);
    ctx.moveTo(width/2,0.05*height);
    ctx.lineTo(width/2,0.95*height);
    ctx.stroke();
    
    ctx.lineWidth=1;
    ctx.beginPath();
    ctx.moveTo(0.05*width,height/2);
    ctx.lineTo(0.05*width+20,height/2-6);
    ctx.lineTo(0.05*width+20,height/2+6);
    ctx.fill();
    
    ctx.moveTo(0.95*width,height/2);
    ctx.lineTo(0.95*width-20,height/2-6);
    ctx.lineTo(0.95*width-20,height/2+6);
    ctx.fill();
    
    ctx.moveTo(width/2,0.05*height);
    ctx.lineTo(width/2-6,0.05*height+20);
    ctx.lineTo(width/2+6,0.05*height+20);
    ctx.fill();
    
    ctx.moveTo(width/2,0.95*height);
    ctx.lineTo(width/2-6,0.95*height-20);
    ctx.lineTo(width/2+6,0.95*height-20);
    ctx.fill();
});