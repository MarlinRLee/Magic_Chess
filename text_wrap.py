from pygame import Rect
import pygame

# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
#From / Based on https://www.pygame.org/wiki/TextWrap
def drawTextAdjust(surface, text, color, rect, aa=False, bkg=None,
             minFont = 10, startingFont = 18):
    rect = Rect(rect)
    
    curFontsize = startingFont
    while curFontsize >= minFont:
        
        font = pygame.font.SysFont(None, curFontsize)
        # get the height of the font
        
        
        blitzText = loop_text(surface, text, color, rect, font, aa=aa, bkg=bkg, blitz=False)

        if blitzText == "":
            break
        curFontsize -= 1
    blitzText = loop_text(surface, text, color, rect, font, aa=aa, bkg=bkg, blitz=True)
    return blitzText



def loop_text(surface, text, color, rect, font, aa=False, bkg=None, blitz = False):
    fontHeight = font.size("Tg")[1]
    lineSpacing = -2
    y = rect.top
    #if text.rfind("\n"):
    #    print(text.rfind("\n"))
    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            if text[i] == "\n":
                text = text[:i] + " " + text[i+1:]
                i += 1
                break
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1
        
        # render the line and blit it to the surface
        if blitz:
            if bkg:
                image = font.render(text[:i], 1, color, bkg)
                image.set_colorkey(bkg)
            else:
                image = font.render(text[:i], aa, color)

            surface.blit(image, (rect.left, y))
        
        y += fontHeight + lineSpacing
        # remove the text we just blitted
        text = text[i:]
    return text