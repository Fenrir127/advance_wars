import unittest
import math
import main
from setting import INFANTRY
import static_ai_agr_v2 as agr_ai
import static_ai_run as run_ai

import time


class TestGame(unittest.TestCase):

    def test_highlight(self):

        # Create the game to test functions in
        self.game_runaway = main.Game()
        self.game_runaway.new('scenario_runaway.txt')
        self.game_attack = main.Game()
        self.game_attack.new('scenario_attack.txt')
        self.game_stalemate = main.Game()
        self.game_stalemate.new('scenario_stalemate.txt')

        # Testing highlight() for Runaway scenario map
        self.game_runaway.highlight(INFANTRY, 3, 99, 0, 1)
        runaway01_highlighted_tile = [(0, 1), (0, 0), (0, 2), (1, 1), (1, 0), (2, 1), (3, 1), (1, 2), (1, 3), (0, 3), (0, 4)]
        for tile in runaway01_highlighted_tile:
            self.assertTrue(self.game_runaway.map.is_highlight(tile[0], tile[1]))
        self.game_runaway.erase_highlights()

        self.game_runaway.highlight(INFANTRY, 3, 99, 5, 3)
        runaway53_highlighted_tile = [(5, 3), (5, 2), (5, 1), (4, 1), (6, 1), (4, 2), (6, 2), (5, 4), (4, 4), (6, 3), (6, 4),
                                      (6, 5), (5, 5), (4, 5), (5, 6)]
        for tile in runaway53_highlighted_tile:
            self.assertTrue(self.game_runaway.map.is_highlight(tile[0], tile[1]))
        self.game_runaway.erase_highlights()

        # Testing highlight() for Attack scenario map
        self.game_attack.highlight(INFANTRY, 3, 99, 1, 3)
        attack13_highlighted_tile = [(1, 3), (1, 2), (1, 1), (0, 1), (2, 1), (0, 2), (0, 1), (0, 3), (2, 2), (0, 4),
                                     (1, 4), (0, 5), (2, 3), (2, 4), (1, 5), (2, 5), (1, 6)]
        for tile in attack13_highlighted_tile:
            self.assertTrue(self.game_attack.map.is_highlight(tile[0], tile[1]))
        self.game_attack.erase_highlights()

        self.game_attack.highlight(INFANTRY, 3, 99, 3, 3)
        attack33_highlighted_tile = [(3, 3), (3, 2), (3, 1), (4, 2), (2, 3), (1, 3), (4, 3), (5, 3), (4, 4), (3, 4), (3, 5)]
        for tile in attack33_highlighted_tile:
            self.assertTrue(self.game_attack.map.is_highlight(tile[0], tile[1]))
        self.game_attack.erase_highlights()

        self.game_attack.highlight(INFANTRY, 3, 99, 6, 0)
        attack60_highlighted_tile = [(6, 0), (5, 0), (5, 1), (6, 1), (4, 1), (5, 2), (6, 2), (5, 2), (6, 3)]
        for tile in attack60_highlighted_tile:
            self.assertTrue(self.game_attack.map.is_highlight(tile[0], tile[1]))
        self.game_attack.erase_highlights()

        # Testing highlight() for Stalemate scenario map
        self.game_stalemate.highlight(INFANTRY, 3, 99, 3, 3)
        stalemate33_highlighted_tile = [(0, 3), (1, 2), (1, 3), (1, 4), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (3, 0),
                                        (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (4, 1), (4, 2), (4, 3), (4, 4),
                                        (4, 5), (5, 2), (5, 3), (5, 4), (6, 3)]
        for tile in stalemate33_highlighted_tile:
            self.assertTrue(self.game_stalemate.map.is_highlight(tile[0], tile[1]))
        self.game_stalemate.erase_highlights()

        self.game_stalemate.highlight(INFANTRY, 3, 99, 6, 5)
        stalemate65_highlighted_tile = [(6, 5), (6, 4), (6, 3), (6, 2), (5, 3), (5, 4), (4, 4), (5, 5), (4, 5), (3, 5), (4, 6),
                                        (5, 6), (6, 6)]
        for tile in stalemate65_highlighted_tile:
            self.assertTrue(self.game_stalemate.map.is_highlight(tile[0], tile[1]))
        self.game_stalemate.erase_highlights()

        # Testing highlight() with enemy close by
        self.game_stalemate.map.reset(enx=4, eny=3)
        self.game_stalemate.highlight(INFANTRY, 3, 99, 3, 3)
        enemy_close_highlighted_tile = [(0, 3), (1, 2), (1, 3), (1, 4), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (3, 0),
                                        (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (4, 1), (4, 2), (4, 4),
                                        (4, 5), (5, 2), (5, 4)]
        for tile in enemy_close_highlighted_tile:
            self.assertTrue(self.game_stalemate.map.is_highlight(tile[0], tile[1]))
        self.assertFalse(self.game_stalemate.map.is_highlight(4, 3))
        self.assertFalse(self.game_stalemate.map.is_highlight(5, 3))
        self.assertFalse(self.game_stalemate.map.is_highlight(6, 3))
        self.game_stalemate.map.reset()

        # Testing highlight() with ally close by
        self.game_stalemate.map.reset(_x=4, _y=3)
        self.game_stalemate.highlight(INFANTRY, 3, 99, 3, 3)
        enemy_close_highlighted_tile = [(0, 3), (1, 2), (1, 3), (1, 4), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (3, 0),
                                        (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (4, 1), (4, 2), (4, 3), (4, 4),
                                        (4, 5), (5, 2), (5, 3), (5, 4), (6, 3)]
        for tile in enemy_close_highlighted_tile:
            self.assertTrue(self.game_stalemate.map.is_highlight(tile[0], tile[1]))
        self.game_stalemate.map.reset()

        # Delete the games, no longer needed
        del self.game_runaway
        del self.game_attack
        del self.game_stalemate

    def test_highlight_enemy(self):

        # Create the game to test functions in
        self.game_runaway = main.Game()
        self.game_runaway.new('scenario_runaway.txt')
        self.game_attack = main.Game()
        self.game_attack.new('scenario_attack.txt')
        self.game_stalemate = main.Game()
        self.game_stalemate.new('scenario_stalemate.txt')

        # Testing highlight_enemy() for Runaway scenario map
        self.game_runaway.highlight_enemy(INFANTRY, 3, 99, 2, 1)
        runaway21_highlighted_enemy_tile = [(2, 1), (2, 0), (1, 0), (0, 0), (0, 1), (1, 1), (1, 2), (3, 0), (4, 0), (5, 0),
                                            (4, 1), (3, 1), (3, 2), (0, 2), (0, 3), (2, 2), (2, 3), (1, 3), (1, 4), (5, 1),
                                            (6, 1), (5, 2), (4, 2)]
        for tile in runaway21_highlighted_enemy_tile:
            self.assertTrue(self.game_runaway.map.is_atk_highlight(tile[0], tile[1]))
        self.game_runaway.erase_highlights()

        # Testing highlight_enemy() for Attack scenario map
        self.game_attack.highlight_enemy(INFANTRY, 3, 99, 5, 3)
        attack53_highlighted_enemy_tile = [(5, 3), (5, 2), (5, 1), (5, 0), (4, 0), (6, 0), (4, 1), (3, 1), (4, 2), (6, 1),
                                           (6, 2), (3, 2), (3, 3), (4, 3), (4, 4), (6, 3), (6, 4),
                                           (3, 4), (3, 5), (5, 4), (5, 5), (4, 5), (4, 6), (6, 5), (6, 6), (5, 6)]
        for tile in attack53_highlighted_enemy_tile:
            self.assertTrue(self.game_attack.map.is_atk_highlight(tile[0], tile[1]))
        self.game_attack.erase_highlights()

        # Testing highlight_enemy() for Stalemate scenario map
        self.game_stalemate.highlight_enemy(INFANTRY, 3, 99, 3, 3)
        stalemate33_highlighted_enemy_tile = [(3, 3), (3, 2), (3, 1), (3, 0), (2, 0), (4, 0), (2, 1), (1, 1), (2, 2), (4, 1),
                                              (5, 1), (4, 2), (1, 2), (0, 2), (1, 3), (2, 3), (2, 4), (5, 2), (6, 2), (5, 3),
                                              (4, 3), (4, 4), (0, 3), (0, 4), (1, 4), (1, 5), (3, 4), (3, 5), (2, 5), (2, 6),
                                              (6, 3), (6, 4), (5, 4), (5, 5), (4, 5), (4, 6), (3, 6)]
        for tile in stalemate33_highlighted_enemy_tile:
            self.assertTrue(self.game_stalemate.map.is_atk_highlight(tile[0], tile[1]))
        self.game_stalemate.erase_highlights()

        # Delete the games, no longer needed
        del self.game_runaway
        del self.game_attack
        del self.game_stalemate

    def test_direct_atk_enemy_highlight(self):
        # Create the game to test functions in
        self.game_runaway = main.Game()
        self.game_runaway.new('scenario_runaway.txt')
        self.game_attack = main.Game()
        self.game_attack.new('scenario_attack.txt')

        # Testing direct_atk_enemy_highlight for Runaway scenario map with 1 enemy
        self.game_runaway.map.reset(6, 1, 6, 0)
        self.game_runaway.direct_atk_enemy_highlight(6, 1)
        stalemate61_direct_atk_with_enemy_tile = [(5, 0), (5, 1), (5, 2), (6, 2), (6, 1)]
        for tile in stalemate61_direct_atk_with_enemy_tile:
            self.assertFalse(self.game_runaway.map.is_atk_highlight(tile[0], tile[1]))
        self.assertTrue(self.game_runaway.map.is_atk_highlight(6, 0))
        self.game_runaway.map.reset()

        # Testing direct_atk_enemy_highlight for Attack scenario map with no enemy
        self.game_attack.map.reset(_x=3, _y=3)
        self.game_attack.direct_atk_enemy_highlight(3, 3)
        attack33_direct_atk_no_enemy_tile = [(2, 2), (3, 2), (4, 2), (2, 3), (3, 3), (4, 3), (2, 4), (3, 4), (4, 4)]
        for tile in attack33_direct_atk_no_enemy_tile:
            self.assertFalse(self.game_attack.map.is_atk_highlight(tile[0], tile[1]))
        self.game_attack.map.reset()

        # Testing direct_atk_enemy_highlight for Attack scenario map with 1 enemy
        self.game_attack.map.reset(3, 3, 4, 3)
        self.game_attack.direct_atk_enemy_highlight(3, 3)
        attacke33_direct_atk_with_enemy_tile = [(2, 2), (3, 2), (4, 2), (2, 3), (3, 3), (2, 4), (3, 4), (4, 4)]
        for tile in attacke33_direct_atk_with_enemy_tile:
            self.assertFalse(self.game_attack.map.is_atk_highlight(tile[0], tile[1]))
        self.assertTrue(self.game_attack.map.is_atk_highlight(4, 3))
        self.game_attack.map.reset()

        # # Delete the games, no longer needed
        # del self.game_runaway
        # del self.game_attack

    def test_atk_target(self):
        # Create the game to test functions in
        self.game_attack = main.Game()
        self.game_attack.new('scenario_attack.txt')
        self.game_stalemate = main.Game()
        self.game_stalemate.new('scenario_stalemate.txt')

        # Attack plain vs plain
        self.game_stalemate.map.reset(3, 3, 4, 3)
        self.game_stalemate.atk_target(3, 3, 4, 3)
        unit1 = self.game_stalemate.map.get_unit(3, 3)
        unit2 = self.game_stalemate.map.get_unit(4, 3)
        self.assertTrue(unit1.hp > unit2.hp)
        self.assertEqual(8, math.ceil(unit1.hp / 10))
        self.assertEqual(5, math.ceil(unit2.hp / 10))

        # Attack plain vs mountain, plain attacking
        self.game_attack.map.reset(5, 3, 4, 3)
        self.game_attack.atk_target(5, 3, 4, 3)
        unit1 = self.game_attack.map.get_unit(5, 3)
        unit2 = self.game_attack.map.get_unit(4, 3)
        self.assertAlmostEqual(unit1.hp, unit2.hp)
        self.assertEqual(7, math.ceil(unit1.hp / 10))
        self.assertEqual(7, math.ceil(unit2.hp / 10))

        # Attack one low, no counter
        self.game_stalemate.map.reset(3, 3, 4, 3)
        unit1 = self.game_stalemate.map.get_unit(3, 3)
        unit2 = self.game_stalemate.map.get_unit(4, 3)
        unit2.hp = 10
        self.game_stalemate.atk_target(3, 3, 4, 3)
        self.assertEqual(100, unit1.hp)
        self.assertIsNone(self.game_stalemate.map.get_unit(4, 3))

        # Attack one low, low attack first
        self.game_stalemate.map.reset(3, 3, 4, 3)
        unit1 = self.game_stalemate.map.get_unit(3, 3)
        unit2 = self.game_stalemate.map.get_unit(4, 3)
        unit2.hp = 10
        self.game_stalemate.atk_target(4, 3, 3, 3)
        self.assertNotEqual(100, unit1.hp)
        self.assertIsNone(self.game_stalemate.map.get_unit(4, 3))

        # Attack river vs plain
        self.game_attack.map.reset(6, 1, 6, 0)
        unit1 = self.game_attack.map.get_unit(6, 1)
        unit2 = self.game_attack.map.get_unit(6, 0)
        self.game_attack.atk_target(6, 1, 6, 0)
        self.assertAlmostEqual(45, unit2.hp)
        self.assertNotEqual(100, unit1.hp)
        self.assertTrue(unit1.hp > unit2.hp)

        # Delete the games, no longer needed
        del self.game_attack
        del self.game_stalemate

    def test_move_unit(self):

        # Create the game to test functions in
        self.game_stalemate = main.Game()
        self.game_stalemate.new('scenario_stalemate.txt')

        # Normal movement
        self.game_stalemate.map.reset(_x=3, _y=3)
        self.game_stalemate.map.move_unit(3, 3, 4, 3)
        self.assertIsNone(self.game_stalemate.map.get_unit(3, 3))
        self.assertTrue(self.game_stalemate.map.get_unit(4, 3))
        self.game_stalemate.map.reset()

        # Normal movement x 2
        self.game_stalemate.map.reset(_x=3, _y=3)
        self.game_stalemate.map.move_unit(3, 3, 4, 3)
        self.game_stalemate.map.move_unit(4, 3, 6, 3)
        self.assertIsNone(self.game_stalemate.map.get_unit(3, 3))
        self.assertIsNone(self.game_stalemate.map.get_unit(4, 3))
        self.assertTrue(self.game_stalemate.map.get_unit(6, 3))
        self.game_stalemate.map.reset()

        # Free movement
        self.game_stalemate.map.reset(_x=0, _y=0)
        self.game_stalemate.map.move_unit(0, 0, 6, 6)
        self.assertIsNone(self.game_stalemate.map.get_unit(0, 0))
        self.assertTrue(self.game_stalemate.map.get_unit(6, 6))
        self.game_stalemate.map.reset()

        # Delete the games, no longer needed
        del self.game_stalemate

    def test_remove_unit(self):

        # Create the game to test functions in
        self.game_stalemate = main.Game()
        self.game_stalemate.new('scenario_stalemate.txt')

        # Direct removal
        self.game_stalemate.map.reset(3, 3, 4, 3)
        unit1 = self.game_stalemate.map.get_unit(3, 3)
        unit2 = self.game_stalemate.map.get_unit(4, 3)
        self.game_stalemate.map.remove_unit(4, 3)
        self.assertIsNone(self.game_stalemate.map.get_unit(4, 3))
        self.assertTrue(self.game_stalemate.map.get_unit(3, 3))

        # Destroyed removal
        self.game_stalemate.map.reset(3, 3, 4, 3)
        unit2 = self.game_stalemate.map.get_unit(4, 3)
        unit2.hp = 10
        self.game_stalemate.atk_target(3, 3, 4, 3)
        self.assertIsNone(self.game_stalemate.map.get_unit(4, 3))

        # Delete the games, no longer needed
        del self.game_stalemate

    def test_get_legal_move_ai(self):
        # Create the game to test functions in
        self.game_runaway = main.Game()
        self.game_runaway.new('scenario_runaway.txt')
        self.game_attack = main.Game()
        self.game_attack.new('scenario_attack.txt')
        self.game_stalemate = main.Game()
        self.game_stalemate.new('scenario_stalemate.txt')

        # Test get_legal_move() for the AI in Runaway scenario Map enemy not in range
        runaway1166_legal_move = agr_ai.test_get_legal_move('scenario_runaway.txt', 3, 1, 1, 6, 6)
        self.game_runaway.highlight(INFANTRY, 3, 99, 1, 1)
        for x in range(7):
            for y in range(7):
                if self.game_runaway.map.is_highlight(x, y):
                    self.assertTrue((x, y) in runaway1166_legal_move)
                else:
                    self.assertFalse((x, y) in runaway1166_legal_move)
        self.game_runaway.erase_highlights()

        # Test get_legal_move() for the AI in Runaway scenario Map enemy in range
        self.game_runaway.map.reset(1, 1, 2, 1)
        runaway1121_legal_move = agr_ai.test_get_legal_move('scenario_runaway.txt', 3, 1, 1, 2, 1)
        self.game_runaway.highlight(INFANTRY, 3, 99, 1, 1)
        for x in range(7):
            for y in range(7):
                if self.game_runaway.map.is_highlight(x, y):
                    self.assertTrue((x, y) in runaway1121_legal_move)
                else:
                    self.assertFalse((x, y) in runaway1121_legal_move)
        self.game_runaway.erase_highlights()
        self.game_runaway.map.reset()

        # Test get_legal_move() for the AI in Attack scenario Map enemy not in range
        attack1166_legal_move = agr_ai.test_get_legal_move('scenario_attack.txt', 3, 1, 1, 6, 6)
        self.game_attack.highlight(INFANTRY, 3, 99, 1, 1)
        for x in range(7):
            for y in range(7):
                if self.game_attack.map.is_highlight(x, y):
                    self.assertTrue((x, y) in attack1166_legal_move)
                else:
                    self.assertFalse((x, y) in attack1166_legal_move)
        self.game_attack.erase_highlights()

        # Test get_legal_move() for the AI in Attack scenario Map enemy not in range
        attack3366_legal_move = agr_ai.test_get_legal_move('scenario_attack.txt', 3, 3, 3, 6, 6)
        self.game_attack.highlight(INFANTRY, 3, 99, 3, 3)
        for x in range(7):
            for y in range(7):
                if self.game_attack.map.is_highlight(x, y):
                    self.assertTrue((x, y) in attack3366_legal_move)
                else:
                    self.assertFalse((x, y) in attack3366_legal_move)
        self.game_attack.erase_highlights()

        # Test get_legal_move() for the AI in Attack scenario Map enemy in range
        self.game_attack.map.reset(6, 0, 6, 1)
        attack6061_legal_move = agr_ai.test_get_legal_move('scenario_runaway.txt', 3, 6, 0, 6, 1)
        self.game_attack.highlight(INFANTRY, 3, 99, 6, 0)
        for x in range(7):
            for y in range(7):
                if self.game_attack.map.is_highlight(x, y):
                    self.assertTrue((x, y) in attack6061_legal_move)
                else:
                    self.assertFalse((x, y) in attack6061_legal_move)
        self.game_attack.erase_highlights()
        self.game_attack.map.reset()

        # Test get_legal_move() for the AI in Stalemate scenario Map enemy not in range
        stalemate3366_legal_move = agr_ai.test_get_legal_move('scenario_attack.txt', 3, 3, 3, 6, 6)
        self.game_attack.highlight(INFANTRY, 3, 99, 3, 3)
        for x in range(7):
            for y in range(7):
                if self.game_attack.map.is_highlight(x, y):
                    self.assertTrue((x, y) in stalemate3366_legal_move)
                else:
                    self.assertFalse((x, y) in stalemate3366_legal_move)
        self.game_attack.erase_highlights()

        # Test get_legal_move() for the AI in Stalemate scenario Map enemy in range
        self.game_attack.map.reset(6, 0, 6, 1)
        stalemate6061_legal_move = agr_ai.test_get_legal_move('scenario_runaway.txt', 3, 6, 0, 6, 1)
        self.game_attack.highlight(INFANTRY, 3, 99, 6, 0)
        for x in range(7):
            for y in range(7):
                if self.game_attack.map.is_highlight(x, y):
                    self.assertTrue((x, y) in stalemate6061_legal_move)
                else:
                    self.assertFalse((x, y) in stalemate6061_legal_move)
        self.game_attack.erase_highlights()
        self.game_attack.map.reset()

        # Delete the games, no longer needed
        del self.game_runaway
        del self.game_attack
        del self.game_stalemate

    def test_get_action_agr(self):

        # Testing get_action for the Agressive AI on Runaway Scenario map
        runaway1166_legal_move = agr_ai.test_get_legal_move('scenario_runaway.txt', 3, 1, 1, 6, 6)
        move = agr_ai.test_get_action(runaway1166_legal_move, 1, 1, 100, 6, 6, 10)
        self.assertIn(move, ((4, 1, 0, 0), (1, 4, 0, 0)))

        # Testing get_action for the Agressive AI on Runaway Scenario map
        runaway1166_legal_move = agr_ai.test_get_legal_move('scenario_runaway.txt', 3, 5, 3, 1, 3)
        move = agr_ai.test_get_action(runaway1166_legal_move, 5, 3, 100, 1, 3, 10)
        self.assertIn(move, ((4, 1, 0, 0), (4, 5, 0, 0)))

        # Testing get_action for the Agressive AI on Runaway Scenario map enemy in range
        runaway1166_legal_move = agr_ai.test_get_legal_move('scenario_runaway.txt', 3, 1, 1, 1, 3)
        move = agr_ai.test_get_action(runaway1166_legal_move, 1, 1, 100, 1, 3, 10)
        self.assertIn(move, ((1, 2, 0, 1), (0, 3, 1, 0)))

        # Testing get_action for the Agressive AI on Stalemate Scenario map enemy in range
        runaway1166_legal_move = agr_ai.test_get_legal_move('scenario_stalemate.txt', 3, 1, 1, 1, 3)
        move = agr_ai.test_get_action(runaway1166_legal_move, 1, 1, 100, 1, 3, 10)
        self.assertIn(move, ((1, 2, 0, 1), (0, 3, 1, 0), (2, 3, -1, 0)))

        # Testing get_action for the Agressive AI on Stalemate Scenario map
        runaway1166_legal_move = agr_ai.test_get_legal_move('scenario_stalemate.txt', 3, 1, 1, 6, 6)
        move = agr_ai.test_get_action(runaway1166_legal_move, 1, 1, 100, 6, 6, 10)
        self.assertIn(move, ((1, 4, 0, 0), (2, 3, 0, 0), (3, 2, 0, 0), (4, 1, 0, 0)))

        # Testing get_action for the Agressive AI on Stalemate Scenario map enemy higher hp
        runaway1166_legal_move = agr_ai.test_get_legal_move('scenario_stalemate.txt', 3, 6, 5, 6, 6)
        move = agr_ai.test_get_action(runaway1166_legal_move, 6, 5, 10, 6, 6, 100)
        self.assertIn(move, ((3, 5, 0, 0), (4, 4, 0, 0), (5, 3, 0, 0), (6, 2, 0, 0)))

    def test_get_action_run(self):

        # Testing get_action for the Run AI on Attack Scenario map
        legal_move = agr_ai.test_get_legal_move('scenario_attack.txt', 3, 1, 1, 3, 3)
        dangerous_move = run_ai.test_get_vulnerable_tile('scenario_attack.txt', 3, 1, 1, 3, 3)
        move = run_ai.test_get_action(legal_move, dangerous_move, 1, 1, 10, 3, 3, 100)
        self.assertEqual(move, (1, 1, 0, 0))

        legal_move = agr_ai.test_get_legal_move('scenario_attack.txt', 3, 1, 1, 6, 6)
        dangerous_move = run_ai.test_get_vulnerable_tile('scenario_attack.txt', 3, 1, 1, 6, 6)
        move = run_ai.test_get_action(legal_move, dangerous_move, 1, 1, 10, 6, 6, 100)
        self.assertEqual(move, (1, 1, 0, 0))

        legal_move = agr_ai.test_get_legal_move('scenario_attack.txt', 3, 1, 1, 1, 3)
        dangerous_move = run_ai.test_get_vulnerable_tile('scenario_attack.txt', 3, 1, 1, 1, 3)
        move = run_ai.test_get_action(legal_move, dangerous_move, 1, 1, 10, 1, 3, 100)
        self.assertEqual(move, (4, 1, 0, 0))

        legal_move = agr_ai.test_get_legal_move('scenario_attack.txt', 3, 4, 5, 1, 5)
        dangerous_move = run_ai.test_get_vulnerable_tile('scenario_attack.txt', 3, 4, 5, 1, 5)
        move = run_ai.test_get_action(legal_move, dangerous_move, 4, 5, 10, 1, 5, 100)
        self.assertEqual(move, (5, 3, 0, 0))

        legal_move = agr_ai.test_get_legal_move('scenario_attack.txt', 3, 1, 3, 3, 3)
        dangerous_move = run_ai.test_get_vulnerable_tile('scenario_attack.txt', 3, 1, 3, 3, 3)
        move = run_ai.test_get_action(legal_move, dangerous_move, 1, 3, 10, 3, 3, 100)
        self.assertIn(move, ((1, 1, 0, 0), (1, 5, 0, 0)))

    def test_get_vulnerable_move(self):
        # Create the game to test functions in
        self.game_attack = main.Game()
        self.game_attack.new('scenario_attack.txt')

        # Test get_vulnerable_move() for the AI in Attack scenario Map
        self.game_attack.map.reset(1, 1, 3, 3)
        attack1166_dangerous_move = run_ai.test_get_vulnerable_tile('scenario_attack.txt', 3, 1, 1, 3, 3)
        self.game_attack.highlight_enemy(INFANTRY, 3, 99, 3, 3)
        for x in range(7):
            for y in range(7):
                if self.game_attack.map.is_atk_highlight(x, y):
                    self.assertTrue((x, y) in attack1166_dangerous_move)
                else:
                    self.assertFalse((x, y) in attack1166_dangerous_move)
        self.game_attack.erase_highlights()

        # Test get_vulnerable_move() for the AI in Attack scenario Map
        self.game_attack.map.reset(1, 1, 5, 3)
        attack1166_dangerous_move = run_ai.test_get_vulnerable_tile('scenario_attack.txt', 3, 1, 1, 5, 3)
        self.game_attack.highlight_enemy(INFANTRY, 3, 99, 5, 3)
        for x in range(7):
            for y in range(7):
                if self.game_attack.map.is_atk_highlight(x, y):
                    self.assertTrue((x, y) in attack1166_dangerous_move)
                else:
                    self.assertFalse((x, y) in attack1166_dangerous_move)
        self.game_attack.erase_highlights()

        # Test get_vulnerable_move() for the AI in Attack scenario Map
        self.game_attack.map.reset(1, 1, 6, 0)
        attack1166_dangerous_move = run_ai.test_get_vulnerable_tile('scenario_attack.txt', 3, 1, 1, 6, 0)
        self.game_attack.highlight_enemy(INFANTRY, 3, 99, 6, 0)
        for x in range(7):
            for y in range(7):
                if self.game_attack.map.is_atk_highlight(x, y):
                    self.assertTrue((x, y) in attack1166_dangerous_move)
                else:
                    self.assertFalse((x, y) in attack1166_dangerous_move)
        self.game_attack.erase_highlights()

        # Delete the games, no longer needed
        del self.game_attack


if __name__ == '__main__':
    unittest.main()
