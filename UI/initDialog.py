# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'initDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QDoubleSpinBox,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_InitValueDialog(object):
    def setupUi(self, InitValueDialog):
        if not InitValueDialog.objectName():
            InitValueDialog.setObjectName(u"InitValueDialog")
        InitValueDialog.resize(291, 444)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(InitValueDialog.sizePolicy().hasHeightForWidth())
        InitValueDialog.setSizePolicy(sizePolicy)
        InitValueDialog.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))
        self.verticalLayout = QVBoxLayout(InitValueDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.thresholdGroupBox = QGroupBox(InitValueDialog)
        self.thresholdGroupBox.setObjectName(u"thresholdGroupBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.thresholdGroupBox.sizePolicy().hasHeightForWidth())
        self.thresholdGroupBox.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setFamilies([u"Arial"])
        self.thresholdGroupBox.setFont(font)
        self.verticalLayout_3 = QVBoxLayout(self.thresholdGroupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.initBatteryNameLabel = QLabel(self.thresholdGroupBox)
        self.initBatteryNameLabel.setObjectName(u"initBatteryNameLabel")

        self.verticalLayout_3.addWidget(self.initBatteryNameLabel)

        self.initBatteryNameLineEdit = QLineEdit(self.thresholdGroupBox)
        self.initBatteryNameLineEdit.setObjectName(u"initBatteryNameLineEdit")

        self.verticalLayout_3.addWidget(self.initBatteryNameLineEdit)

        self.label = QLabel(self.thresholdGroupBox)
        self.label.setObjectName(u"label")

        self.verticalLayout_3.addWidget(self.label)

        self.initBatteryNameComboBox = QComboBox(self.thresholdGroupBox)
        self.initBatteryNameComboBox.setObjectName(u"initBatteryNameComboBox")

        self.verticalLayout_3.addWidget(self.initBatteryNameComboBox)

        self.initCurrentThresholdLayout = QGridLayout()
        self.initCurrentThresholdLayout.setObjectName(u"initCurrentThresholdLayout")
        self.initCurrentMaxLabel = QLabel(self.thresholdGroupBox)
        self.initCurrentMaxLabel.setObjectName(u"initCurrentMaxLabel")

        self.initCurrentThresholdLayout.addWidget(self.initCurrentMaxLabel, 3, 0, 5, 1)

        self.initCurrentThresholdLabel = QLabel(self.thresholdGroupBox)
        self.initCurrentThresholdLabel.setObjectName(u"initCurrentThresholdLabel")

        self.initCurrentThresholdLayout.addWidget(self.initCurrentThresholdLabel, 0, 0, 3, 2)

        self.initCurrentMaxLineEdit = QLineEdit(self.thresholdGroupBox)
        self.initCurrentMaxLineEdit.setObjectName(u"initCurrentMaxLineEdit")
        self.initCurrentMaxLineEdit.setAcceptDrops(False)
        self.initCurrentMaxLineEdit.setInputMethodHints(Qt.ImhDigitsOnly)

        self.initCurrentThresholdLayout.addWidget(self.initCurrentMaxLineEdit, 3, 1, 5, 1)


        self.verticalLayout_3.addLayout(self.initCurrentThresholdLayout)

        self.initVoltageThresholdLayout = QGridLayout()
        self.initVoltageThresholdLayout.setObjectName(u"initVoltageThresholdLayout")
        self.initVoltageMiniLabel = QLabel(self.thresholdGroupBox)
        self.initVoltageMiniLabel.setObjectName(u"initVoltageMiniLabel")

        self.initVoltageThresholdLayout.addWidget(self.initVoltageMiniLabel, 2, 0, 1, 1)

        self.initVoltageThresholdLabel = QLabel(self.thresholdGroupBox)
        self.initVoltageThresholdLabel.setObjectName(u"initVoltageThresholdLabel")

        self.initVoltageThresholdLayout.addWidget(self.initVoltageThresholdLabel, 0, 0, 2, 2)

        self.initVoltageMiniLineEdit = QLineEdit(self.thresholdGroupBox)
        self.initVoltageMiniLineEdit.setObjectName(u"initVoltageMiniLineEdit")
        self.initVoltageMiniLineEdit.setAcceptDrops(False)
        self.initVoltageMiniLineEdit.setInputMethodHints(Qt.ImhDigitsOnly)

        self.initVoltageThresholdLayout.addWidget(self.initVoltageMiniLineEdit, 2, 1, 1, 1)

        self.initVoltageMaxLabel = QLabel(self.thresholdGroupBox)
        self.initVoltageMaxLabel.setObjectName(u"initVoltageMaxLabel")

        self.initVoltageThresholdLayout.addWidget(self.initVoltageMaxLabel, 3, 0, 1, 1)

        self.initVoltageMaxLineEdit = QLineEdit(self.thresholdGroupBox)
        self.initVoltageMaxLineEdit.setObjectName(u"initVoltageMaxLineEdit")
        self.initVoltageMaxLineEdit.setAcceptDrops(False)
        self.initVoltageMaxLineEdit.setInputMethodHints(Qt.ImhDigitsOnly)

        self.initVoltageThresholdLayout.addWidget(self.initVoltageMaxLineEdit, 3, 1, 1, 1)


        self.verticalLayout_3.addLayout(self.initVoltageThresholdLayout)

        self.initTempThresholdLayout = QGridLayout()
        self.initTempThresholdLayout.setObjectName(u"initTempThresholdLayout")
        self.initTempMiniLineEdit = QLineEdit(self.thresholdGroupBox)
        self.initTempMiniLineEdit.setObjectName(u"initTempMiniLineEdit")
        self.initTempMiniLineEdit.setAcceptDrops(False)
        self.initTempMiniLineEdit.setInputMethodHints(Qt.ImhDigitsOnly)

        self.initTempThresholdLayout.addWidget(self.initTempMiniLineEdit, 1, 1, 1, 1)

        self.initTempThresholdLabel = QLabel(self.thresholdGroupBox)
        self.initTempThresholdLabel.setObjectName(u"initTempThresholdLabel")

        self.initTempThresholdLayout.addWidget(self.initTempThresholdLabel, 0, 0, 1, 2)

        self.initTempMaxLineEdit = QLineEdit(self.thresholdGroupBox)
        self.initTempMaxLineEdit.setObjectName(u"initTempMaxLineEdit")
        self.initTempMaxLineEdit.setAcceptDrops(False)
        self.initTempMaxLineEdit.setInputMethodHints(Qt.ImhDigitsOnly)

        self.initTempThresholdLayout.addWidget(self.initTempMaxLineEdit, 2, 1, 1, 1)

        self.initTempMaxLabel = QLabel(self.thresholdGroupBox)
        self.initTempMaxLabel.setObjectName(u"initTempMaxLabel")

        self.initTempThresholdLayout.addWidget(self.initTempMaxLabel, 2, 0, 1, 1)

        self.initTempMiniLabel = QLabel(self.thresholdGroupBox)
        self.initTempMiniLabel.setObjectName(u"initTempMiniLabel")

        self.initTempThresholdLayout.addWidget(self.initTempMiniLabel, 1, 0, 1, 1)


        self.verticalLayout_3.addLayout(self.initTempThresholdLayout)


        self.verticalLayout.addWidget(self.thresholdGroupBox)

        self.GUISettingGroupBox = QGroupBox(InitValueDialog)
        self.GUISettingGroupBox.setObjectName(u"GUISettingGroupBox")
        sizePolicy1.setHeightForWidth(self.GUISettingGroupBox.sizePolicy().hasHeightForWidth())
        self.GUISettingGroupBox.setSizePolicy(sizePolicy1)
        self.GUISettingGroupBox.setFont(font)
        self.verticalLayout_2 = QVBoxLayout(self.GUISettingGroupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.recordingTimeLayout = QHBoxLayout()
        self.recordingTimeLayout.setObjectName(u"recordingTimeLayout")
        self.recordingTimeInitlabel_2 = QLabel(self.GUISettingGroupBox)
        self.recordingTimeInitlabel_2.setObjectName(u"recordingTimeInitlabel_2")

        self.recordingTimeLayout.addWidget(self.recordingTimeInitlabel_2)

        self.recordingTimeInitDoubleSpinBox = QDoubleSpinBox(self.GUISettingGroupBox)
        self.recordingTimeInitDoubleSpinBox.setObjectName(u"recordingTimeInitDoubleSpinBox")
        self.recordingTimeInitDoubleSpinBox.setInputMethodHints(Qt.ImhDigitsOnly|Qt.ImhFormattedNumbersOnly)
        self.recordingTimeInitDoubleSpinBox.setDecimals(1)
        self.recordingTimeInitDoubleSpinBox.setMinimum(0.500000000000000)
        self.recordingTimeInitDoubleSpinBox.setSingleStep(0.500000000000000)
        self.recordingTimeInitDoubleSpinBox.setValue(1.000000000000000)

        self.recordingTimeLayout.addWidget(self.recordingTimeInitDoubleSpinBox)

        self.recordingTimeInitlabel = QLabel(self.GUISettingGroupBox)
        self.recordingTimeInitlabel.setObjectName(u"recordingTimeInitlabel")

        self.recordingTimeLayout.addWidget(self.recordingTimeInitlabel)


        self.verticalLayout_2.addLayout(self.recordingTimeLayout)

        self.initValuePushButton = QPushButton(self.GUISettingGroupBox)
        self.initValuePushButton.setObjectName(u"initValuePushButton")

        self.verticalLayout_2.addWidget(self.initValuePushButton)


        self.verticalLayout.addWidget(self.GUISettingGroupBox)


        self.retranslateUi(InitValueDialog)

        QMetaObject.connectSlotsByName(InitValueDialog)
    # setupUi

    def retranslateUi(self, InitValueDialog):
        InitValueDialog.setWindowTitle(QCoreApplication.translate("InitValueDialog", u"Initial Value Setting", None))
        self.thresholdGroupBox.setTitle(QCoreApplication.translate("InitValueDialog", u"Battery Specifications", None))
        self.initBatteryNameLabel.setText(QCoreApplication.translate("InitValueDialog", u"Add battery type:", None))
        self.initBatteryNameLineEdit.setPlaceholderText(QCoreApplication.translate("InitValueDialog", u"Add battery type", None))
        self.label.setText(QCoreApplication.translate("InitValueDialog", u"Or choose an existing name:", None))
        self.initBatteryNameComboBox.setPlaceholderText("")
        self.initCurrentMaxLabel.setText(QCoreApplication.translate("InitValueDialog", u"Maximum:", None))
        self.initCurrentThresholdLabel.setText(QCoreApplication.translate("InitValueDialog", u"Pack Current threshold (mA):", None))
        self.initCurrentMaxLineEdit.setText(QCoreApplication.translate("InitValueDialog", u"1500", None))
        self.initCurrentMaxLineEdit.setPlaceholderText(QCoreApplication.translate("InitValueDialog", u"Default value 1500mA", None))
        self.initVoltageMiniLabel.setText(QCoreApplication.translate("InitValueDialog", u"Minimum:", None))
        self.initVoltageThresholdLabel.setText(QCoreApplication.translate("InitValueDialog", u"Cell voltage threshold (mV):", None))
        self.initVoltageMiniLineEdit.setText(QCoreApplication.translate("InitValueDialog", u"1700", None))
        self.initVoltageMiniLineEdit.setPlaceholderText(QCoreApplication.translate("InitValueDialog", u"Default value 1700mV", None))
        self.initVoltageMaxLabel.setText(QCoreApplication.translate("InitValueDialog", u"Maximum:", None))
        self.initVoltageMaxLineEdit.setText(QCoreApplication.translate("InitValueDialog", u"2500", None))
        self.initVoltageMaxLineEdit.setPlaceholderText(QCoreApplication.translate("InitValueDialog", u"Default value 2500mV", None))
        self.initTempMiniLineEdit.setText(QCoreApplication.translate("InitValueDialog", u"-40", None))
        self.initTempMiniLineEdit.setPlaceholderText(QCoreApplication.translate("InitValueDialog", u"Default value -40C", None))
        self.initTempThresholdLabel.setText(QCoreApplication.translate("InitValueDialog", u"IC temperature threshold (\u2103):", None))
        self.initTempMaxLineEdit.setText(QCoreApplication.translate("InitValueDialog", u"120", None))
        self.initTempMaxLineEdit.setPlaceholderText(QCoreApplication.translate("InitValueDialog", u"Default value 120C", None))
        self.initTempMaxLabel.setText(QCoreApplication.translate("InitValueDialog", u"Maximum:", None))
        self.initTempMiniLabel.setText(QCoreApplication.translate("InitValueDialog", u"Minimum:", None))
        self.GUISettingGroupBox.setTitle(QCoreApplication.translate("InitValueDialog", u"GUI Settings", None))
        self.recordingTimeInitlabel_2.setText(QCoreApplication.translate("InitValueDialog", u"Recording Time Interval:", None))
        self.recordingTimeInitlabel.setText(QCoreApplication.translate("InitValueDialog", u"Hour (s)", None))
        self.initValuePushButton.setText(QCoreApplication.translate("InitValueDialog", u"Done", None))
    # retranslateUi

