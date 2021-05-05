extends KinematicBody2D

onready var brain = get_node("Brain")

var alive := false

var jump_power := 1000.0
var gravity := 1000.0
var speed := 400.0
var velocity := Vector2.ZERO

var current_pipe_index := 0
var current_pipe = null
var fitness := 0.0

func _ready() -> void:
	add_to_group("birds")
	alive = true
	
func get_brain():
	return get_node("Brain")

func get_current_pipe():
	var pipe = get_parent().get_pipe(current_pipe_index)
	return pipe

func _process(_delta: float) -> void:
	update()

func _draw() -> void:
	if alive and current_pipe:
		var pipe_position = (current_pipe.get_position() - get_position()) / 2
		draw_line(Vector2(0,0), pipe_position + Vector2(0,50), Color(255,255,255))
		draw_line(Vector2(0,0), pipe_position + Vector2(0,-50), Color(255,255,255))
	
func _physics_process(delta: float) -> void:
	if alive:
		current_pipe = get_current_pipe()
		if current_pipe:
			var pipe_position = (current_pipe.get_position() - get_position()) / 2
			if brain.predict([get_position().y, pipe_position.x, pipe_position.y + 50, pipe_position.y - 50]) > 0.5:
				velocity.y = -speed 
			else:
				velocity.y += gravity * delta
			move_and_slide(velocity)
			if position.y < 0 or position.y > 800:
				died()
	
func reward() -> void:
	current_pipe_index += 1
	fitness += 5.0
	
func died() -> void:
	fitness -= 5
	alive = false
	set_position(Vector2(-100,0))


