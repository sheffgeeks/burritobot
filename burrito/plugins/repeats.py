import irc3

repeatables = (
    ":-) :) :o) :] :3 :c) :> =] 8) =) :} :^) :っ) "
    ":-D :D 8-D 8D x-D xD X-D XD =-D =D =-3 =3 B^D "
    ":-)) "
    ">:[ :-( :(  :-c :c :-<  :っC :< :-[ :[ :{ "
    ";( "
    ":-|| :@ >:( "
    ":'-( :'( "
    ":'-) :') "
    "D:< D: D8 D; D= DX v.v D-': "
    ">:O :-O :O :-o :o 8-0 O_O o-o O_o o_O o_o O-O "
    ":* :^* ( '}{' ) "
    ";-) ;) *-) *) ;-] ;] ;D ;^) :-, "
    ">:P :-P :P X-P x-p xp XP :-p :p =p :-Þ :Þ :þ :-þ :-b :b d: "
    ">:\ >:/ :-/ :-. :/ :\ =/ =\ :L =L :S >.< "
    ":| :-| "
    ":$ "
    ":-X :X :-# :# "
    "O:-) 0:-3 0:3 0:-) 0:) 0;^) "
    ">:) >;) >:-) "
    "}:-) }:) 3:-) 3:) "
    "o/\o ^5 >_>^ ^<_< "
    "|;-) |-O "
    ":-& :& "
    "#-) "
    "%-) %) "
    ":-###.. :###.. "
    "<:-| "
    "ಠ_ಠ "
    "<*)))-{ ><(((*> ><> "
    "\o/ "
    "*\0/* "
    "@}-;-'--- @>-->-- "
    "~(_8^(I) "
    "5:-) ~:-\ "
    "//0-0\\ "
    "*<|:-) "
    "=:o] "
    ",:-) 7:^] "
    "<3 </3 ").split()


@irc3.plugin
class RepeatAfterTwo(object):
    lastnick = None
    lastmsg = None
    def __init__(self, bot):
        self.bot = bot

    @irc3.event(irc3.rfc.PRIVMSG)
    def process(self, mask=None, event=None, target=None, data=None):
        if mask.nick == self.bot.nick or mask.nick == self.lastnick:
            self.lastmsg, self.lastnick = None, None
        elif data not in repeatables:
            self.lastmsg, self.lastnick = None, None
        elif data == self.lastmsg:
            self.bot.privmsg(target, data)
            self.lastmsg, self.lastnick = None, None
        else:
            self.lastmsg, self.lastnick = data, mask.nick
