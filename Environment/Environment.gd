extends Node2D

var Bird := load("res://src/Bird/Bird.tscn")
var Pipe := load("res://src/Pipe/Pipe.tscn")

onready var generation_label = get_node("GenerationLabel")
onready var population_label = get_node("PopulationLabel")
onready var score_label = get_node("ScoreLabel")
onready var Generation := get_node("Generation")

const POP_SIZE := 200

var rng := RandomNumberGenerator.new()
var time := 2.0

var pipes := []
var birds := []
var birds_alive = 0
var generation = 0
var score = 0

var running := false

func _ready() -> void:
	reset()

func add_pipe():
	var new_pipe = Pipe.instance()
	new_pipe.position = Vector2(650, rng.randi_range(200,600))
	add_child(new_pipe)
	pipes.append(new_pipe)
	
	score_label.text = "Score : " + str(score)
	score += 1
	return new_pipe

func reset():
	running = false
	birds_alive = 0
	
	score = 0
	score_label.text = "Score : " + str(score)
	
	for pipe in pipes:
		if is_instance_valid(pipe):
			pipe.queue_free()
	pipes = []

	var data_paths = Generation.create_generation(POP_SIZE, birds)

	for bird in birds:
		if is_instance_valid(bird):
			bird.queue_free()
	birds = []

	for data_path in data_paths:
		var bird = Bird.instance()
		var brain = bird.get_brain()
		brain.init(data_path)
		birds.append(bird)
		add_child(bird)
	
	generation_label.text = "Generation : " + str(generation)
	population_label.text = "Population : " + str(POP_SIZE)
	generation += 1
	
	time = 2.0
	running = true

func get_birds_alive():
	birds_alive = 0
	for bird in birds:
		if bird.alive:
			birds_alive += 1
	population_label.text = "Population : " + str(birds_alive)
	return birds_alive

func _process(delta: float) -> void:
	if running:
		if get_birds_alive() == 0:
			reset()
			return
		time += delta
		if time > 1.5:
			time = 0
			add_pipe()

func get_pipe(index):
	if index < len(pipes):
		return pipes[index]

func python_print(s):
	print(s)
