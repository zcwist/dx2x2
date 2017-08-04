/* global $ */
$(document).ready(function(){
    // $(".skill").draggable();
    // $(".skill").click(function(){
    //     console.log("hello world")
    // }
    var survey_id = $("#survey_id").text();

    var scale = 0.7;
    $("#canvasgrid").height(function(){
        return scale*$(document).height();
    });
    $("#skills").height(function(){
        return scale*$(document).height();
    });
    
    var skills_num;
    $.getJSON("/skills/"+survey_id,function(result){
        skills_num = result.length;
        $.each(result,function(i, field){
            $('.skills').append(
                '<div class="row skill group" id="'+field.id+'">'+
            '<h5 class = "ui-accordion-header">' + field.skill_name + '</h5>' +
            '<div>' + field.skill_descrip +'</div>' +
            "</div>");
        });
        
        $(".skills").accordion({
            animate: 300,
            collapsible: true,
            active: false,
            header: "> div > h5"

        });
        $(".skill").draggable({
            helper: function(event){
                var ret = $(this).clone();
                
                $(this).toggleClass("ghost");
                ret.accordion({active:true,icons:false});
                ret.accordion({active:true,icons:false});

                
                ret.children("h5").removeClass("ui-accordion-header");
                ret.addClass("skill_in_canvas");
                ret.children("h5").addClass("dx");

                var skill_text = ret.children("h5").text().split(" ");
                // console.log(skill_text.length);
                ret.children("h5").empty();
                var i;
                for (i = 0; i < Math.ceil(skill_text.length/2); i++){
                    // console.log(i);
                    ret.children("h5").append(skill_text[i]);
                    if (i<Math.ceil(skill_text.length/2)-1){
                        ret.children("h5").append(" ");
                    }
                }
                ret.children("h5").append("<br>");
                for (i = Math.ceil(skill_text.length/2); i < skill_text.length ; i++){
                    // console.log(i);
                    ret.children("h5").append(skill_text[i]);
                    if (i<Math.ceil(skill_text.length)-1){
                        ret.children("h5").append(" ");
                    }
                }
                ret.appendTo("#dxcanvas");
                console.log(ret);

                return ret;
            },
            stop: function(event, ui){
                var position = ui.helper.position();
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
        
        $(".skill").hover(function () {
            if ($(this).hasClass("ghost")){
                var id = $(this).attr("id");
                var skill_in_canvas = $("#"+id +".skill_in_canvas>h5");
                // skill_in_canvas.effect("highlight",{},2000);
                skill_in_canvas.toggleClass("highlight-skill");
            }
        });
        
        //Check if this user surveyed
        $.getJSON("/userinfo",function(result) {
            var user_id = result;
            var survey_info = {user_id:user_id, survey_id:survey_id};
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
                        var skill_id = key;
                        // console.log($(".skill#"+skill_id));
                        $(".skill#"+skill_id).toggleClass("ghost");
                        $(".skill#"+skill_id).draggable("disable");
                        
                        //reload canvas
                        var skill_in_canvas = $(".skill#"+skill_id).clone();
                        
                        skill_in_canvas.accordion({active:false,icons:false});
                        skill_in_canvas.removeClass("skill");
                        skill_in_canvas.accordion({active:false,icons:false}); //clear the icons double created by cloning

                        skill_in_canvas.toggleClass("ghost");
                        skill_in_canvas.addClass("skill_in_canvas");
                        skill_in_canvas.draggable({
                            containment: "parent"
                        });
                        skill_in_canvas.children("h5").addClass("dx");
                        skill_in_canvas.children("h5").removeClass("ui-accordion-header");
                        
                        //Return for long skill name
                        var skill_text = skill_in_canvas.children("h5").text().split(" ");
                        skill_in_canvas.children("h5").empty();
                        var i;
                        for (i = 0; i < Math.ceil(skill_text.length/2); i++){
                            skill_in_canvas.children("h5").append(skill_text[i]);
                            if (i<Math.ceil(skill_text.length/2)-1){
                                skill_in_canvas.children("h5").append(" ");
                            }
                        }
                        skill_in_canvas.children("h5").append("<br>");
                        for (i = Math.ceil(skill_text.length/2); i < skill_text.length ; i++){
                            skill_in_canvas.children("h5").append(skill_text[i]);
                            if (i<Math.ceil(skill_text.length)-1){
                                skill_in_canvas.children("h5").append(" ");
                            }
                        }
                        
                        
                        
                        var original_canvas_size = canvas_data.canvas_size;
                        var new_canvas_size = {"width":$("#myCanvas").width(),"height":$("#myCanvas").height()};
                        var width_coff=new_canvas_size.width/original_canvas_size.width;
                        var height_coff=new_canvas_size.height/original_canvas_size.height;
                        var position = value;
                        skill_in_canvas.detach().css({'position':'absolute', 'top':position.top*height_coff,'left':position.left*width_coff});
                        skill_in_canvas.appendTo($("#dxcanvas"));
                        skill_in_canvas.dblclick(function(){
                            // console.log($(this).attr("id"));
                            
                            skill_id = $(this).attr("id");
                            // console.log($(".skill#"+skill_id));
                            // $(".skill#"+skill_id).toggleClass("ghost");
                            $(".skill#"+skill_id).draggable("enable");
                            $("#"+skill_id+".skill > h5").toggleClass("highlight-skill");
                            this.remove();
                        });
                        
                        skill_in_canvas.hover(function(){
                            var skill_id = $(this).attr("id");
                            // console.log($("#"+skill_id+".skill"));
                            $("#"+skill_id+".skill").toggleClass("ghost");
                            $("#"+skill_id+".skill > h5").toggleClass("highlight-skill");
                            
                            
                        });
                        
                        skill_in_canvas.click(function(){
                            var skill_id = $(this).attr("id");
                            var skill = $("#"+skill_id+".skill");
                            var skills = $("div.skills");
                            skills.animate({
                                scrollTop:skills.scrollTop()+ skill.offset().top - skills.offset().top
                            },200);
                        })
                        
                    });
                }
              }
            });
        });
    });
    
    $("#dxcanvas").droppable({
        drop:function(event,ui){
            if (ui.draggable.hasClass('skill')){
                var dropped = ui.draggable.clone();
                // skill_in_canvas_render($(dropped),ui);
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
                $(dropped).children("h5").removeClass("ui-accordion-header");
                
                //Return for long skill name
                var skill_text = $(dropped).children("h5").text().split(" ");
                console.log(skill_text.length);
                $(dropped).children("h5").empty();
                var i;
                for (i = 0; i < Math.ceil(skill_text.length/2); i++){
                    console.log(i);
                    $(dropped).children("h5").append(skill_text[i]);
                    if (i<Math.ceil(skill_text.length/2)-1){
                        $(dropped).children("h5").append(" ");
                    }
                }
                $(dropped).children("h5").append("<br>");
                for (i = Math.ceil(skill_text.length/2); i < skill_text.length ; i++){
                    console.log(i);
                    $(dropped).children("h5").append(skill_text[i]);
                    if (i<Math.ceil(skill_text.length)-1){
                        $(dropped).children("h5").append(" ");
                    }
                }
                

                $(dropped).dblclick(function(){
                    // console.log($(this).attr("id"));
                    
                    var skill_id = $(this).attr("id");
                    // console.log($(".skill#"+skill_id));
                    // $(".skill#"+skill_id).toggleClass("ghost");
                    $(".skill#"+skill_id).draggable("enable");
                    $("#"+skill_id+".skill > h5").toggleClass("highlight-skill");
                    this.remove();
                });
                
                $(dropped).hover(function(){
                    var skill_id = $(this).attr("id");
                    // console.log($("#"+skill_id+".skill"));
                    $("#"+skill_id+".skill").toggleClass("ghost");
                    $("#"+skill_id+".skill > h5").toggleClass("highlight-skill");
                })
                $(dropped).click(function(){
                    var skill_id = $(this).attr("id");
                    var skill = $("#"+skill_id+".skill");
                    var skills = $("div.skills");
                    skills.animate({
                        scrollTop:skills.scrollTop()+ skill.offset().top - skills.offset().top
                    },200);
                })
            }
        }
    });
    
    
    //reset button
    $("#reset").click(function() {
        console.log("reset button clicked");
        $(".skill_in_canvas").each(function(index) {
            // console.log("in the loop")

            var skill_id = $(this).attr("id");
            // console.log($(".skill#"+skill_id));
            $(".skill#"+skill_id).toggleClass("ghost");
            $(".skill#"+skill_id).draggable("enable");
            this.remove();
        });
    });
    // add the sign out function
    $('#exit').attr('href', '/login');
    //end modificaition
    
    $("#save").click(function(){
        var dict = {};
        dict["survey_id"] = survey_id;
        var canvas_data = {};
        canvas_data["canvas_size"] = {"width":$("#myCanvas").width(),"height":$("#myCanvas").height()};
        var skills_pos = {};
        $(".skill_in_canvas").each(function(index){
            // console.log($(this).attr("id"));
            // console.log($(this).position());
            skills_pos[$(this).attr("id")] = $(this).position();
            skills_pos[$(this).attr("id")]["width"] = $(this).width();
            skills_pos[$(this).attr("id")]["height"] = $(this).height();
            //normalize coordinates
        });
        canvas_data["skills_pos"]=skills_pos;
        // console.log(skills_pos);
        
        var skill_no_pos = [];
        
        $(".skill").not(".ghost").each(function(index){
            skill_no_pos.push($(this).attr("id"));
        });
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
                  alert("Great! 2x2 canvas saved!");
              }

            });
        });
    });
    
    function drawCanvas(){
        var canvas = $("#myCanvas");
        var width = canvas.parent().width();
        var height = canvas.parent().height();
        // console.log(height);
        canvas = document.getElementById("myCanvas");
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


        //draw mark in x direction from -5 to 5:
         var startWidth = 0.05 * width + 25
         var delta = 0.09 * width - 5;

         var markerLength = 0.01 * height
         for (var i = 0; i <= 10; i++) {
             ctx.moveTo(startWidth, height/2);
             ctx.textAlign="center";

             ctx.fillText(i,startWidth, height/2 - 12)
             ctx.lineTo(startWidth, height/2 - markerLength);
             ctx.stroke();
             console.log("here");
             startWidth += delta;

         }

        // draw mark in y direction from -5 to 5"
        var Heightdelta = 0.09 * height - 5;
        var starHeight = 0.05 * height + 25
        for (var i = 10; i >= 0; i--) {
             ctx.moveTo(width/2, starHeight);
             ctx.textAlign="center";
             if (i != 5)
                ctx.fillText(i, width /2  - 12, starHeight)
             ctx.lineTo(width / 2 - markerLength, starHeight);
             ctx.stroke();
             starHeight += Heightdelta;

         }


        function drawTemplate(ctx) {
            $.getJSON("/template/"+survey_id, function(result){
            // console.log(result)
    
            var tp = result.top;
            var bot = result.bottom;
            var left = result.left;
            var right = result.right;
    
            
            ctx.font="12px Comic Sans MS";
            ctx.textAlign="left"; 
            ctx.fillText(left,0.05*width + 24,height/2 + 12);
            ctx.textAlign="right"; 
            ctx.fillText(right,0.95*width - 24 ,height/2 + 12);
            ctx.textAlign="center";
            ctx.fillText(tp, width/2, 0.05*height - 12);
            ctx.textAlign="center";
            ctx.fillText(bot, width/2, 0.95*height + 12);
        
            });
       
        }
        
        drawTemplate(ctx);
    }
    
    drawCanvas();
});