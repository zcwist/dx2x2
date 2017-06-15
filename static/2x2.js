$(document).ready(function(){
    // $(".skill").draggable();
    // $(".skill").click(function(){
    //     console.log("hello world")
    // })
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
                ret.appendTo("#2x2canvas")
                $(this).toggleClass("ghost");
                return ret;
            },
            // start: function(event, ui){
            //     console.log(ui.position)
            //     original_pos = ui.position;
            // },
            stop: function(event, ui){
                position = ui.helper.position()
                if (position.left >0){
                    
                }
                else {
                    $(this).toggleClass("ghost");
                }
            },
            revert: false,
        });
        $(".skill").click(function () {
            console.log(this)
        })
    })
    $("#2x2canvas").droppable({
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
                $(dropped).dblclick(function(){
                    // console.log($(this).attr("id"));
                    
                    skill_id = $(this).attr("id")
                    console.log($(".skill#"+skill_id));
                    $(".skill#"+skill_id).toggleClass("ghost");
                    this.remove();
                })
                
            }
            
        }
    })
    $("#save").click(function(){
        dict = {}
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
    
});