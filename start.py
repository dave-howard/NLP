from nltk_test.nltk_basics import disambiguate, run_tests

text1 = "The solution will include LAN, WAN and Firewall. The LAN will include both fixed and wireless"
text2 = """The traffic will be routed by the L3 device. 
Routes will be advertised by BGP or other dynamic protocol. 
There will be no static routing."""

run_tests(text1, text2)

disambiguate(text1="sing in a lower tone, along with the bass",
             text2="that sea bass was really hard to catch",
             term="bass")