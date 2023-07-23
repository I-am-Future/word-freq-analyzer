from deep_translator import GoogleTranslator

input = '''
The focus of the reading and the lecture is about the orgin of animals on Madagascar island. The reading conveys three doubts that animals could not float to the island. The lecture, however, considers what the reading suggests unconvincing.

First, the reading expresses that land animals can rarely cross the sea accidentally. Animals may be carried to Madagascar by the float logs. But this would not happen very frequently. What's more, in order to reproduce on the island, a couple of animals should be carried to there at the same time. Given that the mammal diversity on the island was quite large, it is unlikely that many animals cross the ocean accidentaly. On the contrary, the lecture disagrees to this point. Recent genetic research reveals that all of the animals on the Madagascar island are derived from only four species. That is, there may be only four species of animal crossed the ocean. In that case, this successful crossing just need happen four times in 40 million years. Even crossing to the island is an unusual event, 4 succesful cases could still happen.

Second, the passage states that the ocean current does not flow towards Madagascar. Therefore, animals on floating debris cannot be carried to the island by the current. Even the current may carry them away from Madagascar. In sharp constrast, the professor claims that although nowadays currents are flowing in the opposite direction, but the direction 60 million years ago was not. The computer simulation proposes that 60 millions years ago, the Madagascar island was a bit of south compared to nowadays. At that time, the current flow was different, that they were toward island. As a result, it is possible that current carried animals to the island. 

Third, the reading thinks that the journey may be too long for animals to survive. It is estimated that the floating voyage takes about three weeks. On the debris, there were no food or fresh water. So, before the animals reached to the island, they would die because of hunger or thirst first. Oppositely, the professor holds the opinion that they would not necessary to die. Some animals have the ability to torpor, which means that they can enter a state of low metabolism rate. In that case, they don't eat nor drink. In addition, it is discovered that animals on the island also have the ability to torpor. So their ancestor can also do that, enduring the hunger and thirsty on the long ocean ride till the island.

'''
words = input.split()
print(words)

print(GoogleTranslator(source='auto', target='zh-CN').translate('\n'.join(words)) )