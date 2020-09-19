from botmother.utils.bot_router import BotRouter
from botmother.tests.request import TelegramTestCase


class BotRouterTest(TelegramTestCase):
    function_runned = False

    def function(self, **args):
        self.function_runned = True

    def test_command(self):
        route = BotRouter(self.load('start_command.json'))
        self.function_runned = False
        route.command('/start', self.function)

        self.assertTrue(self.function_runned)
        self.assertEqual(route.type, "command")

    def test_starts_with(self):
        route = BotRouter(self.load('start_command.json'))
        self.function_runned = False
        route.starts_with('/start', self.function)

        self.assertTrue(self.function_runned)
        self.assertIn(route.type, "command")

    def test_text(self):
        route = BotRouter(self.load('products_text.json'))
        self.function_runned = False
        route.text("⭐  Хиты продаж", self.function)

        self.assertTrue(self.function_runned)
        self.assertIn(route.type, "text")

    def test_callback(self):
        route = BotRouter(self.load('order_info_callback.json'))
        self.function_runned = False
        route.callback('first_order_product_count_', self.function)

        self.assertTrue(self.function_runned)
        self.assertIn(route.type, "callback")

    def test_location(self):
        route = BotRouter(self.load('order_location.json'))
        self.function_runned = False
        route.location(self.function)

        self.assertTrue(self.function_runned)
        self.assertIn(route.type, "location")

    def test_contact(self):
        route = BotRouter(self.load('order_contact.json'))
        self.function_runned = False
        route.contact(self.function)

        self.assertTrue(self.function_runned)
        self.assertIn(route.type, "contact")

    def test_any(self):
        route = BotRouter(self.load('start_command.json'))
        self.function_runned = False
        route.any(self.function)

        self.assertTrue(self.function_runned)

    def test_run_handler(self):
        route = BotRouter(self.load('start_command.json'))
        route.chat.last_action = 'main_menu'
        route.chat.save()

        self.function_runned = False
        route.run(self.function, 'main_menu', 'private')

        self.assertTrue(self.function_runned)
