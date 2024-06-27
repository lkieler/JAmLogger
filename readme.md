Alternativ arbeite ich derzeit auch eine einem Persönlichem Projekt namens JAmLogger (Just Another Ham Logger).
Es ist bei weitem noch nicht fertig und erklären könnte ich vieles wahrscheinlich auch nicht, bzw. auf Fragen wie beispielsweiße "Was ist eine class" kann ich keine antwort geben. Den KV teil kan ich...

Was soll das Programm können?
    Ein Simples Logbuch für QSO's, weil mir die aktuellen verfügbaren Programme nicht gefallen/ich nihct zahlen möchte für ein Programm dass zuletzt vor 6y updates bekam...
Wie wird es umgesetzt?
    Mit Kivy (und MDKivy). Warum kivy und nicht Tkinter? Weil kivy platformübergreifend ist und ich plane eine Handyapp zu machen.
Was funktioniert (bzw. noch nicht)?
    Bis jetzt lag der Fokus nur auf GUI anpassungen, deswegen ist die funktionalität praktisch nicht vorhanden bzw. nicht mehr mit dem aktuellen aufbau kompatibel. Dies umfasst vorallem den json teil. Wichtig um das programm zu starten darf keine datei names 'log_data.json' im selben ordner vorhanden sein, da wird das Programm sofort beleidigt und verzieht sich.
    Was auch nicht ganz funktioniert ist z223: strftime kennt das %z argument nicht. Es started zwar aber es wird nichts ausgagaben an der stelle des %z arguments. (%z solle utc offset sein, eg +2000).

!!!DAS PROGRAMM IST IM ALPHA-ALPHA-ALPHA-STATUS v.0.0.0.0.0.0.0.0.0.1!!! (oder so)

Installation (also wie es bei mir funktioniert #alpha-stage):
    python (duh) <-- halbwegs aktuell (in meinem fall 3.12)
    pip install https://github.com/kivymd/KivyMD/archive/master.zip (weil die standartversion in pip zu alt ist)

Kleingedruckte:
    Etwaige Rechtschreibfehler sind vorbehalten. Dient nur zu demonstartionszwecken, nichts ist echt, alles simulation (oder so). ChatGPT anteil: ca 60%-75% (also fast alles abgesehen vom KV teil, aber auch nur weil ich mich auf KV fokusiert habe und erst gester (Montag) mit dem Programm anfing.)
