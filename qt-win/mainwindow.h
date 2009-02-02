/****************************************************************************
    **
    ** Copyright (C) 2004-2005 Trolltech AS. All rights reserved.
    **
    ** This file is part of the documentation of the Qt Toolkit.
    **
    ** This file may be used under the terms of the GNU General Public
** License version 2.0 as published by the Free Software Foundation
** and appearing in the file LICENSE.GPL included in the packaging of
** this file.  Please review the following information to ensure GNU
** General Public Licensing requirements will be met:
** http://www.trolltech.com/products/qt/opensource.html
**
** If you are unsure which license is appropriate for your use, please
** review the following information:
** http://www.trolltech.com/products/qt/licensing.html or contact the
** sales department at sales@trolltech.com.
    **
    ** This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
    ** WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
    **
    ****************************************************************************/

    #ifndef MAINWINDOW_H
    #define MAINWINDOW_H

    #include <QMainWindow>

    class QAction;
    class QMenu;
    class QTextEdit;

    class MainWindow : public QMainWindow
    {
        Q_OBJECT

    public:
        MainWindow();

    protected:
        void closeEvent(QCloseEvent *event);

    private slots:
        void newFile();
        void open();
        bool save();
        bool saveAs();
        void about();
        void documentWasModified();

    private:
        void createActions();
        void createMenus();
        void createToolBars();
        void createStatusBar();
        void readSettings();
        void writeSettings();
        bool maybeSave();
        void loadFile(const QString &fileName);
        bool saveFile(const QString &fileName);
        void setCurrentFile(const QString &fileName);
        QString strippedName(const QString &fullFileName);

        QTextEdit *textEdit;
        QString curFile;

        QMenu *fileMenu;
        QMenu *editMenu;
        QMenu *helpMenu;
        QToolBar *fileToolBar;
        QToolBar *editToolBar;
        QAction *newAct;
        QAction *openAct;
        QAction *saveAct;
        QAction *saveAsAct;
        QAction *exitAct;
        QAction *cutAct;
        QAction *copyAct;
        QAction *pasteAct;
        QAction *aboutAct;
        QAction *aboutQtAct;
    };

    #endif
