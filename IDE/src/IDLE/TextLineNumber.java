/** Instituto Tecnológico de Costa Rica
 *  Lenguajes, Compiladores e Interpretes
 *  Prof. Marco Hernandez Vasquez
 *  I Semestre, 2021
 *
 * @author Steven Badilla, Valeria Ortiz, Andrey Sanchez, Bryan Solano
 */

package IDLE;

import java.awt.*;
import java.awt.event.*;
import java.beans.*;
import java.util.HashMap;
import javax.swing.*;
import javax.swing.border.*;
import javax.swing.event.*;
import javax.swing.text.*;


public class TextLineNumber extends JPanel implements CaretListener, DocumentListener, PropertyChangeListener {
    public final static float LEFT = 0.0f;
    public final static float CENTER = 0.5f;
    public final static float RIGHT = 1.0f;

    private final static Border OUTER = new MatteBorder(0, 0, 0, 2, Color.GRAY);

    private final static int HEIGHT = Integer.MAX_VALUE - 1000000;

    // Componente de texto con la que el componete TextTextLineNumber se sincroniza

    private JTextComponent component;

    //  Propiedades modificables

    private boolean updateFont;
    private int borderGap;
    private Color currentLineForeground;
    private float digitAlignment;
    private int minimumDisplayDigits;

    //  Mantienen el historial para evitar repintar de mas
    private int lastDigits;
    private int lastHeight;
    private int lastLine;

    private HashMap<String, FontMetrics> fonts;

    /**
     *	Constructor.
     *	El ancho mostrado se basa en 3 digitos
     *
     *  @param component: Componente de texto relacionada
     */
    public TextLineNumber(JTextComponent component)
    {
        this(component, 3);
    }

    /**
     *	Constructor.
     *
     *  @param component: Componente de texto relacionada
     *  @param minimumDisplayDigits: Numero de digitos, usado para calcular la anchura minima
     */
    public TextLineNumber(JTextComponent component, int minimumDisplayDigits)
    {
        this.component = component;

        setFont( component.getFont() );

        setBorderGap( 5 );
        setCurrentLineForeground( Color.RED );
        setDigitAlignment( RIGHT );
        setMinimumDisplayDigits( minimumDisplayDigits );

        component.getDocument().addDocumentListener(this);
        component.addCaretListener( this );
        component.addPropertyChangeListener("font", this);
    }

    /**
     *  Getter de la propiedad de actualizacion de fuente
     *
     *  @return updateFont: Propiedad de actualizacion de fuente
     */
    public boolean getUpdateFont()
    {
        return updateFont;
    }

    /**
     *  Setter de la propiedad de actualizacion de fuente
     *
     *  @param updateFont: Boolean para saber si actualizar la fuente
     */
    public void setUpdateFont(boolean updateFont)
    {
        this.updateFont = updateFont;
    }

    /**
     *  Getter del margen
     *
     *  @return borderGap: Valor del margen en pixeles
     */
    public int getBorderGap()
    {
        return borderGap;
    }

    /**
     *  Setter del margen
     *
     *  @param borderGap: Tamaño del margen en pixeles
     */
    public void setBorderGap(int borderGap)
    {
        this.borderGap = borderGap;
        Border inner = new EmptyBorder(0, borderGap, 0, borderGap);
        setBorder( new CompoundBorder(OUTER, inner) );
        lastDigits = 0;
        setPreferredWidth();
    }

    /**
     *  Getter del color de resaltado de la linea actual
     *
     *  @return currentLineForeground: Color de resaltado de la linea actual
     */
    public Color getCurrentLineForeground()
    {
        return currentLineForeground == null ? getForeground() : currentLineForeground;
    }

    /**
     *  Setter del color de resaltado de la linea actual
     *
     *  @param currentLineForeground: Color de resaltado de la linea actual
     */
    public void setCurrentLineForeground(Color currentLineForeground)
    {
        this.currentLineForeground = currentLineForeground;
    }

    /**
     *  Getter de la alineacion de los digitos
     *
     *  @return digitAlignment: Alineacion de los digitos
     */
    public float getDigitAlignment()
    {
        return digitAlignment;
    }

    /**
     *  Setter de la alineacion de los digitos
     *
     *  @param digitAlignment: Alineacion de los digitos
     */
    public void setDigitAlignment(float digitAlignment)
    {
        this.digitAlignment =
                digitAlignment > 1.0f ? 1.0f : digitAlignment < 0.0f ? -1.0f : digitAlignment;
    }

    /**
     *  Getter de los digitos de visualizacion minimos
     *
     *  @return minimumDisplayDigits: Digitos de visualizacion minimos
     */
    public int getMinimumDisplayDigits()
    {
        return minimumDisplayDigits;
    }

    /**
     *  Setter de los digitos de visualizacion minimos
     *
     *  @param minimumDisplayDigits: Digitos de visualizacion minimos
     */
    public void setMinimumDisplayDigits(int minimumDisplayDigits)
    {
        this.minimumDisplayDigits = minimumDisplayDigits;
        setPreferredWidth();
    }

    /**
     *  Funcion que calcula el ancho necesario para mostrar el maximo line number
     */
    private void setPreferredWidth()
    {
        Element root = component.getDocument().getDefaultRootElement();
        int lines = root.getElementCount();
        int digits = Math.max(String.valueOf(lines).length(), minimumDisplayDigits);

        //  Actualiza el tamaño cuando el numero de digitos del line number cambio

        if (lastDigits != digits)
        {
            lastDigits = digits;
            FontMetrics fontMetrics = getFontMetrics( getFont() );
            int width = fontMetrics.charWidth( '0' ) * digits;
            Insets insets = getInsets();
            int preferredWidth = insets.left + insets.right + width;

            Dimension d = getPreferredSize();
            d.setSize(preferredWidth, HEIGHT);
            setPreferredSize( d );
            setSize( d );
        }
    }

    /**
     *  Funcion que dibuja los line numbers
     */
    @Override
    public void paintComponent(Graphics g)
    {
        super.paintComponent(g);

        //	Determina el ancho del espacio disponible para dibujar el line number

        FontMetrics fontMetrics = component.getFontMetrics( component.getFont() );
        Insets insets = getInsets();
        int availableWidth = getSize().width - insets.left - insets.right;

        //  Determina las filas a dibujar sin los limites recortados.

        Rectangle clip = g.getClipBounds();
        int rowStartOffset = component.viewToModel( new Point(0, clip.y) );
        int endOffset = component.viewToModel( new Point(0, clip.y + clip.height) );

        while (rowStartOffset <= endOffset)
        {
            try
            {
                if (isCurrentLine(rowStartOffset))
                    g.setColor( getCurrentLineForeground() );
                else
                    g.setColor( getForeground() );

                //  Obtiene el line number como string y determina el desplazamiento en
                //  X y Y para dibujar el string.

                String lineNumber = getTextLineNumber(rowStartOffset);
                int stringWidth = fontMetrics.stringWidth( lineNumber );
                int x = getOffsetX(availableWidth, stringWidth) + insets.left;
                int y = getOffsetY(rowStartOffset, fontMetrics);
                g.drawString(lineNumber, x, y);

                // Avanza de fila

                rowStartOffset = Utilities.getRowEnd(component, rowStartOffset) + 1;
            }
            catch(Exception e) {break;}
        }
    }

    /**
     *  Funcion para saber si el signo de intercalacion se ubica en la linea que
     *  se va a pintar, para poder resaltar el line number
     */
    private boolean isCurrentLine(int rowStartOffset)
    {
        int caretPosition = component.getCaretPosition();
        Element root = component.getDocument().getDefaultRootElement();

        if (root.getElementIndex( rowStartOffset ) == root.getElementIndex(caretPosition))
            return true;
        else
            return false;
    }

    /**
     * Getter del line number que se va a dibujar
     * Retorna un string vacio si se hizo un ajuste en las lineas de texto
     */
    protected String getTextLineNumber(int rowStartOffset)
    {
        Element root = component.getDocument().getDefaultRootElement();
        int index = root.getElementIndex( rowStartOffset );
        Element line = root.getElement( index );

        if (line.getStartOffset() == rowStartOffset)
            return String.valueOf(index + 1);
        else
            return "";
    }

    /**
     * Getter del desplazamiento en X para ajustar el line number cuando se dibuja
     */
    private int getOffsetX(int availableWidth, int stringWidth)
    {
        return (int)((availableWidth - stringWidth) * digitAlignment);
    }

    /**
     *  Getter del desplazamiento en Y para la fila actual
     */
    private int getOffsetY(int rowStartOffset, FontMetrics fontMetrics)
            throws BadLocationException
    {
        // Obtiene el rectangulo que delimita la fila

        Rectangle r = component.modelToView( rowStartOffset );
        int lineHeight = fontMetrics.getHeight();
        int y = r.y + r.height;
        int descent = 0;

        // El texto se coloca encima de la parte inferior del
        // rectángulo delimitador en función del descenso de la (s) fuente (s)
        // contenidas en la fila.

        if (r.height == lineHeight)  // se usa la fuente por default
        {
            descent = fontMetrics.getDescent();
        }
        else  // Se revisan todos los atributos para determinar cambios de fuente
        {
            if (fonts == null)
                fonts = new HashMap<String, FontMetrics>();

            Element root = component.getDocument().getDefaultRootElement();
            int index = root.getElementIndex( rowStartOffset );
            Element line = root.getElement( index );

            for (int i = 0; i < line.getElementCount(); i++)
            {
                Element child = line.getElement(i);
                AttributeSet as = child.getAttributes();
                String fontFamily = (String)as.getAttribute(StyleConstants.FontFamily);
                Integer fontSize = (Integer)as.getAttribute(StyleConstants.FontSize);
                String key = fontFamily + fontSize;

                FontMetrics fm = fonts.get( key );

                if (fm == null)
                {
                    Font font = new Font(fontFamily, Font.PLAIN, fontSize);
                    fm = component.getFontMetrics( font );
                    fonts.put(key, fm);
                }

                descent = Math.max(descent, fm.getDescent());
            }
        }

        return y - descent;
    }

    /**
     * Funcion que implementa la interfaz CaretListener
    */
    @Override
    public void caretUpdate(CaretEvent e)
    {
        //  Obtiene la linea de ubicacion del signo de intercalacion

        int caretPosition = component.getCaretPosition();
        Element root = component.getDocument().getDefaultRootElement();
        int currentLine = root.getElementIndex( caretPosition );

        //  Repinta

        if (lastLine != currentLine)
        {
//			repaint();
            getParent().repaint();
            lastLine = currentLine;
        }
    }

    /**
     * Funciones que implementa la interfaz DocumentListener
     */
    @Override
    public void changedUpdate(DocumentEvent e)
    {
        documentChanged();
    }

    @Override
    public void insertUpdate(DocumentEvent e)
    {
        documentChanged();
    }

    @Override
    public void removeUpdate(DocumentEvent e)
    {
        documentChanged();
    }

    /**
     *  Funcion para cambiar los numeros de linea en caso de cambios en el documento
     */
    private void documentChanged()
    {
        //  Verifica que no hayan actualizacione en el documento en el momento
        //  en que DocumentEvent es ejecutado

        SwingUtilities.invokeLater(new Runnable()
        {
            @Override
            public void run()
            {
                try
                {
                    int endPos = component.getDocument().getLength();
                    Rectangle rect = component.modelToView(endPos);

                    if (rect != null && rect.y != lastHeight)
                    {
                        setPreferredWidth();
//						repaint();
                        getParent().repaint();
                        lastHeight = rect.y;
                    }
                }
                catch (BadLocationException ex) { /* nothing to do */ }
            }
        });
    }

    /**
     * Funciones que implementa la interfaz PropertyChangeListener
     */
    @Override
    public void propertyChange(PropertyChangeEvent evt)
    {
        if (evt.getNewValue() instanceof Font)
        {
            if (updateFont)
            {
                Font newFont = (Font) evt.getNewValue();
                setFont(newFont);
                lastDigits = 0;
                setPreferredWidth();
            }
            else
            {
//				repaint();
                getParent().repaint();
            }
        }
    }
}