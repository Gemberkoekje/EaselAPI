# Pass 2 - the sky. One graded passage, tilted 4 degrees so it parallels the
# far edge rather than the frame. Erase the ruled horizon first: it is never
# going to be found across the middle third.
s.erase(region=span("D3", "G5"))
m_sky()
print(s.look())
print(s.look(values=True))
