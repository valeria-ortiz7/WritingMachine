package IDLE;

import javax.swing.*;
import java.awt.*;



public class TextEditor extends JPanel {

    private JPanel panel1;
    private JTextArea taEditor;
    private JScrollPane scrollpane;
    private TextLineNumber tln;

    public TextEditor(){
        setLayout(new BorderLayout(0,0));

        scrollpane = new JScrollPane();
        add(scrollpane, BorderLayout.CENTER);

        taEditor = new JTextArea();
        scrollpane.setViewportView(taEditor);

        tln = new TextLineNumber(taEditor);
        tln.setBorderGap(-1);
        tln.setDigitAlignment(CENTER_ALIGNMENT);
        tln.setCurrentLineForeground(Color.GREEN);
        scrollpane.setRowHeaderView(tln);

    }

    public String getTexto(){
        return taEditor.getText();
    }

    public void refresh(String texto){
        taEditor.setText(texto);
    }
}
