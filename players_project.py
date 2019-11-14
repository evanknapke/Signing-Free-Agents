#!/usr/bin/python3
import sys
import unittest

class Player():
	"""
	.. _Player:

	A free agent baseball player.

	:ivar name: player's name
	:ivar position: player's field position
	:ivar cost: player's salary if signed
	:ivar vorp: player's rank (value over replacement player)
	"""
	def __init__(self, name, position, cost, vorp):
		"""
		Create a new Player object.

		:param name: the player's name
		:type name: str
		:param postion: the player's field position.
		:type position: int
		:param cost: the amount of money it will cost to sign the player.
		:type cost: int
		:param vorp: the players VORP (value over replacement player) rank.
		:type vorp: int
		"""
		self.name=name
		self.position=position
		self.cost=cost
		self.vorp=vorp
		
	def __repr__(self):
		""" Return a string representation of the list 
		:return: a string representation of the list, suitable for use in checking equality between 2 player objects
		:rtype: str
		"""
		return repr( (self.name, self.position, self.cost, self.vorp) )
		

def sort_players( players_list ):
	"""
	.. _sort_players:
	
	Auxiliary procedure that sorts the players by value (vorp/cost) in descending order

	:param players_list:  a list of Player objects holding information about the player, (:math:`n_i`, :math:`p_i`, :math:'c_i', :math:'v_i') the player's name, position, cost, and VORP, respectively
	:type players_list: list
	:return:  a sequence of the same tuples, sorted according to vorp/cost, in descending order.
	:rtype: list
	"""
	return sorted(players_list, key=lambda x: x.vorp/x.cost, reverse=True)


def free_agent_vorp(players, budget, num_positions):
	"""
	.. _free_agent_vorp:
	
	Sign those players that will maximize the cumulative team VORP.
		
	:param players: a list of Player objects holding information about the player, (:math:`n_i`, :math:`p_i`, :math:'c_i', :math:'v_i') the player's name, position, cost, and VORP, respectively
	:type players: list
	:param budget: the maximum amount of money to be spent
	:type budget: int
	:param num_postions: the amount, and index, of the positions being considered
	:type num_positions: int
	:return: 3-tuple of the total VORP of the players signed, the total amount of money spent, a list of which players are signed
	:rtype: tuple
	"""
	# sort the list of players
	players = sort_players(players)
	
	vorp_total = 0
	price_total = 0
	signed_players = []
	filled_positions = []
	i = 0

	def get_best_team(players, budget):
		nonlocal vorp_total
		nonlocal price_total
		nonlocal signed_players
		nonlocal filled_positions
		nonlocal i
		
		# if current price of added players is equal to the team budget
		if price_total == budget:
			return
		# if there are no more players left to sign
		if i >= len(players):
			return
		# if there are no more positions left to be signed
		if len(filled_positions) > num_positions:
			return

		# if position is not already filled, the total price does not go over budget if player is added, and player position is equal or below the amount being considered
		if (players[i].position not in filled_positions) and (price_total + players[i].cost <= budget) and (players[i].position <= num_positions):
			
			# sign player
			price_total += players[i].cost
			vorp_total += players[i].vorp
			signed_players.append(players[i].name)
			filled_positions.append(players[i].position)
			
		i += 1
		get_best_team(players, budget)
		
		return ( (vorp_total, price_total, signed_players) )
		
	return get_best_team(players, budget)


class Player_Project_Test( unittest.TestCase ):

	def test_sort_players(self):
		player_list = [Player("Susie Second", 1, 200000, 90), Player("Felix First", 2, 100000, 100), Player("Logan Last", 3, 700000, 10), Player("Thor Third", 4, 200000, 50)]	
		self.assertEqual( repr(sort_players(player_list)), repr([Player("Felix First", 2, 100000, 100), Player("Susie Second", 1, 200000, 90), Player("Thor Third", 4, 200000, 50), Player("Logan Last", 3, 700000, 10)]) )
	
	def test_fav_1(self):
		"""
		All players in list are signed: total sum of player salaries equals budget, and all positions are unique.
		"""
		player_list = [Player("Albert Angel", 1, 100000, 10), Player("Barry Batter", 2, 100000, 20), Player("Chad Cleats", 3, 200000, 50), Player("Dennis Dodger", 4, 300000, 70)]
		self.assertEqual( free_agent_vorp(player_list, 700000, 4), (150, 700000, ["Chad Cleats", "Dennis Dodger", "Barry Batter", "Albert Angel"]) )

	def test_fav_2(self):
		"""
		Multiple players with the same position.
		"""
		player_list = [Player("Eric Eephus", 1, 200000, 10), Player("Fred First", 2, 100000, 20), Player("Gary Glove", 2, 200000, 50), Player("Henry Hitter", 4, 300000, 70), Player("Ian Inning", 1, 100000, 30), Player("Jack Junk", 3, 200000, 5)]
		self.assertEqual( free_agent_vorp(player_list, 800000, 4), (155, 800000, ["Ian Inning", "Gary Glove", "Henry Hitter", "Jack Junk"]) )
		
	def test_fav_3(self):
		"""
		Total player cost sum becomes above the budget (in the middle of array).
		"""
		player_list = [Player("Kevin Knuckler", 1, 100000, 10), Player("Larry Left", 2, 100000, 20), Player("Morgan Mariner", 2, 300000, 50), Player("Nick National", 4, 200000, 70), Player("Oscar Outfield", 1, 700000, 99), Player("Peter Pitcher", 3, 100000, 5), Player("Quinn Quality", 6, 400000, 44), Player("Ricky Right", 7, 200000, 69)]
		self.assertEqual( free_agent_vorp(player_list, 1000000, 7), (213, 1000000, ["Nick National", "Ricky Right", "Larry Left", "Quinn Quality", "Kevin Knuckler" ]) )

	def test_fav_4(self):
		"""
		Players in list that play a position above the positions being considered.
		"""
		player_list = [Player("Sam Slinger", 1, 100000, 10), Player("Terry Toss", 6, 100000, 20), Player("Urvine Umpire", 2, 200000, 50), Player("Victor Vorp", 10, 200000, 60), Player("Wesley Walk", 9, 100000, 99)]
		self.assertEqual( free_agent_vorp(player_list, 300000, 5), (60, 300000, ["Urvine Umpire", "Sam Slinger"]) )

	def test_fav_5(self):
		"""
		Total player cost sum of signed players is less than the team budget.
		"""
		player_list = [Player("Xavier X", 1, 100000, 10), Player("Zane Zero", 2, 100000, 20), Player("Alex Athlete", 3, 200000, 50)]
		self.assertEqual( free_agent_vorp(player_list, 900000, 3), (80, 400000, ["Alex Athlete", "Zane Zero", "Xavier X"]) )
		
	def test_fav_6(self):
		"""
		No player is able to be signed.
		"""
		player_list = [Player("Blake Base", 1, 300000, 10), Player("Corey Catcher", 2, 500000, 20), Player("Dexter Dugout", 3, 200000, 50)]
		self.assertEqual( free_agent_vorp(player_list, 100000, 4), (0, 0, []) )
		
	def test_fav_7(self):
		"""
		Actual full size team being considered (over 9 positions).
		"""
		player_list = [Player("Evan Even", 1, 100000, 10), Player("Favian Fly", 2, 100000, 20), Player("Guy Ground", 2, 300000, 50), Player("Hans Hand", 4, 200000, 70), Player("Igor Infield", 1, 700000, 99), Player("Jerry Jump", 3, 100000, 5), Player("Kenny K", 6, 400000, 44), Player("Louis Lefty", 7, 200000, 69), Player("Manny Mound", 9, 500000, 107), Player("Negan Nubber", 12, 300000, 54), Player("Omar Oppo", 6, 100000, 44), Player("Perry Park", 5, 300000, 63), Player("Quaid Quit", 11, 200000, 44)]
		self.assertEqual( free_agent_vorp(player_list, 2500000, 13), (486, 2100000, ["Omar Oppo", "Hans Hand", "Louis Lefty", "Quaid Quit", "Manny Mound", "Perry Park", "Favian Fly", "Negan Nubber", "Evan Even", "Jerry Jump"]) )



def main():
        unittest.main()

if __name__ == '__main__':
        main()
