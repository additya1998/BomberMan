BOMBER MAN

Controls:
	'w' - Move up
	'a' - Move left
	's' - Move down
	'd' - Move right
	'b'	- Drop bomb
	'p' - Request a power-up

Types of Enemies:
	1. Health : Some enemies need a single explosion to kill, others required double explosions to kill.
	2. Speed : Enemies can move with different speeds.

Levels:
	1. Level 1: 5 enemies, all have single health and slow speed.
	2. Level 2: 5 enemies, all have single health and fast speed.
	3. Level 3: 10 enemies, all have single health and slow speed.
	4. Level 4: 10 enemies, 5 have slow speed, 5 have fast speed, all have single health.
	5. Level 5: 10 enemies, 5 have slow speed, 5 have fast speed, 5 have single health, 5 have double health.
	6. Level 6: 15 enemies, all have double health and double speed.

PowerUps:
	Health powerup : When the user presses 'p', a power-up pops up at a random empty cell, which if the user takes adds an extra life
	for the player throughout the game, and disappears if the user fails to reach the cell within 5 seconds.

Scoring:
	Killing an enemy = 100 points
	Destoring a brick = 20 points

	The user is gives 300 seconds to complete a single level, if he cannot do it, the user looses a life.
	If the user does it the time left is added to his score as a bonus.

User wins the game when he crosses all the 6 levels.
User looses the game when he looses all his lives.

Classes Used:
	1. Board
	2. Bomber
	3. Bomb
	4. Brick
	5. Enemy
	6. Game
	7. Input
	8. Person
	9. Position
	10. Powerup


Encapsulation:
	No class function can access or directly modify any data member of another class, all data members and some functions are private to their own class.
	
Polymorphism:
	Many classes have functions with same names and parameters, so it does not matter on the class on whose instance it has been called. 

Modularity:
	The code is organized into various modules i.e classes which in turn are a component and different components are independent of each other up to a certain extent.

Inheritance:
	Position class is inherited by the Person class, which in turn is inherited by the BomberMan and Enemy class.

Bonus:
	All bonus points are implemented.