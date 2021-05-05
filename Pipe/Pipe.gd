extends Node2D

var speed := -275.0
var velocity := Vector2.ZERO
var pipe_top := 0.0
var pipe_bottom := 0.0

func _ready() -> void:
	var position_y = get_position().y
	pipe_top = position_y + 50
	pipe_bottom = position_y - 50
	
func _physics_process(delta: float) -> void:
	velocity.x = speed * delta
	position += velocity
	if position.x < -50:
		queue_free()
	
func _on_reward_body_entered(bird: Node) -> void:
	if bird.is_in_group("birds"):
		bird.reward()

func _on_bottom_body_entered(bird: Node) -> void:
	if bird.is_in_group("birds"):
		bird.died()

func _on_top_body_entered(bird: Node) -> void:
	if bird.is_in_group("birds"):
		bird.died()
