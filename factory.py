import xml.etree.ElementTree as ET
import player_pb2
from player import Player


class PlayerFactory:
    def to_json(self, players):
        player_dicts = []
        for player in players:
            player_dict = {
                "nickname": player.nickname,
                "email": player.email,
                "date_of_birth": player.date_of_birth.strftime("%Y-%m-%d"),
                "xp": player.xp,
                "class": player.cls
            }
            player_dicts.append(player_dict)
        return player_dicts

    def from_json(self, list_of_dict):
        players = []
        for data in list_of_dict:
            player = Player(data.get('nickname'), data.get('email'), data.get('date_of_birth'), data.get('xp'),
                            data.get('class'))
            players.append(player)
        return players

    def to_xml(self, list_of_players):
        root = ET.Element('data')
        for player in list_of_players:
            player_elm = ET.SubElement(root, 'player')
            nickname_element = ET.SubElement(player_elm, 'nickname')
            nickname_element.text = player.nickname
            email_element = ET.SubElement(player_elm, 'email')
            email_element.text = player.email
            dob_element = ET.SubElement(player_elm, 'date_of_birth')
            dob_element.text = player.date_of_birth.strftime("%Y-%m-%d")
            xp_element = ET.SubElement(player_elm, 'xp')
            xp_element.text = str(player.xp)
            class_element = ET.SubElement(player_elm, 'class')
            class_element.text = player.cls
        return ET.tostring(root).decode('utf-8')

    def from_xml(self, xml_string):
        players = []
        root = ET.fromstring(xml_string)
        for player_elem in root.findall('player'):
            nickname = player_elem.find('nickname').text
            email = player_elem.find('email').text
            date_of_birth = player_elem.find('date_of_birth').text
            xp = int(player_elem.find('xp').text)
            cls = player_elem.find('class').text
            player = Player(nickname, email, date_of_birth, xp, cls)
            players.append(player)
        return players

    def from_protobuf(self, binary):
        players_message = player_pb2.PlayersList()
        players_message.ParseFromString(binary)
        players = []
        for player_message in players_message.player:
            if player_message.cls == player_pb2.Class.Berserk:
                cls = "Berserk"
            elif player_message.cls == player_pb2.Class.Tank:
                cls = "Tank"
            elif player_message.cls == player_pb2.Class.Paladin:
                cls = "Paladin"
            elif player_message.cls == player_pb2.Class.Mage:
                cls = "Mage"
            else:
                raise ValueError(f"Unknown class enum value: {player_message.cls}")
            player = Player(
                nickname=player_message.nickname,
                email=player_message.email,
                date_of_birth=player_message.date_of_birth,
                xp=player_message.xp,
                cls=cls
            )
            players.append(player)

        return players
        pass

    def to_protobuf(self, list_of_players):
        players_list = player_pb2.PlayersList()

        for player in list_of_players:
            player_message = players_list.player.add()
            player_message.nickname = player.nickname
            player_message.email = player.email
            player_message.date_of_birth = player.date_of_birth.strftime("%Y-%m-%d")
            player_message.xp = player.xp
            if player.cls == "Berserk":
                player_message.cls = player_pb2.Class.Berserk
            elif player.cls == "Tank":
                player_message.cls = player_pb2.Class.Tank
            elif player.cls == "Paladin":
                player_message.cls = player_pb2.Class.Paladin
            elif player.cls == "Mage":
                player_message.cls = player_pb2.Class.Mage
            else:
                raise ValueError(f"Unknown class: {player.cls}")
            # player_message.cls = player.cls

        return players_list.SerializeToString()

