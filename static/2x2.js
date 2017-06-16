$(document).ready(function(){
    // $(".skill").draggable();
    // $(".skill").click(function(){
    //     console.log("hello world")
    // }
    survey_id = $("#survey_id").text();

    scale = 0.7
    $("#canvasgrid").height(function(){
        return scale*$(document).height();
    })
    $("#skills").height(function(){
        return scale*$(document).height();
    })
    
    $.getJSON("/skills/"+survey_id,function(result){
        $.each(result,function(i, field){
            $('.skills').append(
                '<div class="row skill group" id="'+field.id+'">'+
            '<h5 class = "ui-accordion-header">' + field.skill_name + '</h5>' +
            '<div>' + field.skill_descrip +'</div>' +
            "</div>")
        });
        
        $(".skills").accordion({
            animate: 300,
            collapsible: true,
            active: false,
            header: "> div > h5"

        })
        $(".skill").draggable({
            helper: function(event){
                var ret = $(this).clone();
                ret.appendTo("#dxcanvas");
                $(this).toggleClass("ghost");
                ret.accordion({active:true,icons:false});
                ret.accordion({active:true,icons:false});
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
            if ($(this).hasClass("ghost")){
                id = $(this).attr("id");
                console.log(".skill_in_canvas#"+id);
                // skill_in_canvas = $(".skill_in_canvas#"+id);
                // console.log(skill_in_canvas);
                // skill_in_canvas.toggle("ghost");
                $(".skill_in_canvas#"+id).remove();
            }
        })
        
        //Check if this user surveyed
        $.getJSON("/userinfo",function(result) {
            user_id = result;
            survey_info = {user_id:user_id, survey_id:survey_id};
            $.ajax({
              type:"POST",
              url: "/loadcanvas",
              data: JSON.stringify({"survey_info":survey_info}),
              dataType: "json",
              contentType: 'application/json;charset=UTF-8',
              success: function(result){
                // console.log(result);
                if (result.surveyed){
                    // console.log(result);
                    // console.log(result.canvas_data);
                    var canvas_data = result.canvas_data;
                    
                    $.each(canvas_data.skills_pos,function(key, value){
                        //reload skill list
                        skill_id = key;
                        // console.log($(".skill#"+skill_id));
                        $(".skill#"+skill_id).toggleClass("ghost");
                        $(".skill#"+skill_id).draggable("disable");
                        
                        //reload canvas
                        skill_in_canvas = $(".skill#"+skill_id).clone();
                        skill_in_canvas.accordion({active:false,icons:false});
                        skill_in_canvas.removeClass("skill");
                        skill_in_canvas.accordion({active:false,icons:false}); //clear the icons double created by cloning

                        skill_in_canvas.toggleClass("ghost");
                        skill_in_canvas.addClass("skill_in_canvas");
                        skill_in_canvas.draggable({
                            containment: "parent"
                        });
                        skill_in_canvas.children("h5").addClass("dx");
                        
                        original_canvas_size = canvas_data.canvas_size;
                        new_canvas_size = {"width":$("#myCanvas").width(),"height":$("#myCanvas").height()};
                        width_coff=new_canvas_size.width/original_canvas_size.width;
                        height_coff=new_canvas_size.height/original_canvas_size.height;
                        position = value;
                        skill_in_canvas.detach().css({'position':'absolute', 'top':position.top*height_coff,'left':position.left*width_coff});
                        skill_in_canvas.appendTo($("#dxcanvas"));
                        skill_in_canvas.dblclick(function(){
                            // console.log($(this).attr("id"));
                            
                            skill_id = $(this).attr("id")
                            // console.log($(".skill#"+skill_id));
                            $(".skill#"+skill_id).toggleClass("ghost");
                            $(".skill#"+skill_id).draggable("enable");
                            this.remove();
                        })
                        
                    })
                }
              }
            })
        })
    })
    
    $("#dxcanvas").droppable({
        drop:function(event,ui){
            if (ui.draggable.hasClass('skill')){
                var dropped = ui.draggable.clone();
                $(dropped).accordion({active:false, icons: null});
                $(dropped).accordion({active:false, icons: null});
                // $(dropped+">h5").removeClass("ui-state-active");
                $(dropped).toggleClass("ghost");
                $(dropped).removeClass("skill");
                $(dropped).addClass("skill_in_canvas");
                $(dropped).detach().css({'position':'absolute', 'top':ui.position.top,'left':ui.position.left}).appendTo($(this));
                $(dropped).draggable({
                    containment: "parent"
                    });
                $(dropped).children("h5").addClass("dx");
                // $(dropped+">h5").addClass("dx");
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
                    // console.log($(".skill#"+skill_id));
                    $(".skill#"+skill_id).toggleClass("ghost");
                    $(".skill#"+skill_id).draggable("enable");
                    this.remove();
                })
                
                
                
            }
            
        }
    })
    
    //reset button
    $("#reset").click(function() {
        console.log("reset button clicked")
        $(".skill_in_canvas").each(function(index) {
            // console.log("in the loop")

            skill_id = $(this).attr("id")
            // console.log($(".skill#"+skill_id));
            $(".skill#"+skill_id).toggleClass("ghost");
            $(".skill#"+skill_id).draggable("enable");
            this.remove();
        })
    })
    // add the sign out function
    $('#exit').attr('href', '/login');
    //end modificaition
    
    $("#save").click(function(){
        dict = {};
        dict["survey_id"] = survey_id;
        canvas_data = {};
        canvas_data["canvas_size"] = {"width":$("#myCanvas").width(),"height":$("#myCanvas").height()};
        skills_pos = {};
        $(".skill_in_canvas").each(function(index){
            // console.log($(this).attr("id"));
            // console.log($(this).position());
            skills_pos[$(this).attr("id")] = $(this).position();
            //normalize coordinates
        });
        canvas_data["skills_pos"]=skills_pos;
        
        var skill_no_pos = [];
        
        $(".skill").not(".ghost").each(function(index){
            skill_no_pos.push($(this).attr("id"));
        })
        canvas_data["skill_no_pos"] = skill_no_pos;

        dict["canvas_data"] = canvas_data;
        
        $.getJSON("/userinfo",function(result) {
            dict["user_id"] = result;
            $.ajax({
              type:"POST",
              url: "/kaiyue/test",
              data: JSON.stringify({"total":dict}),
              // data: {"total":dict},
              dataType: "json",
              contentType: 'application/json;charset=UTF-8',

              success: function(){
                  alert("Great! 2x2 canvas saved!")
              }

            })
        })
    })
    function drawTemplate(ctx) {
         $.getJSON("/template/"+survey_id, function(result){
        // console.log(result)

        var tp = result.top
        var bot = result.bottom
        var left = result.left
        var right = result.right

        // console.log(tp)
        var rtlength = right.length * 12
        
        ctx.font="12px Comic Sans MS";
        ctx.textAlign="left"; 
        ctx.fillText(left,0.05*width + 24,height/2 + 12);
        ctx.textAlign="right"; 
        ctx.fillText(right,0.95*width - 24 ,height/2 + 12);
        ctx.textAlign="center"
        ctx.fillText(tp, width/2, 0.05*height - 12)
        ctx.textAlign="center"
        ctx.fillText(bot, width/2, 0.95*height + 12)
        
    })
       
    }
    function drawCanvas(){
        var canvas = $("#myCanvas");
        width = canvas.parent().width();
        height = canvas.parent().height();
        // console.log(height);
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
        

        drawTemplate(ctx)
    }
    drawCanvas();
});