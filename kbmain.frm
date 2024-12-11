VERSION 5.00
Begin VB.Form kbmain 
   Caption         =   "Kterm Keyboard Layouter"
   ClientHeight    =   7560
   ClientLeft      =   120
   ClientTop       =   450
   ClientWidth     =   13815
   BeginProperty Font 
      Name            =   "Arial"
      Size            =   12
      Charset         =   0
      Weight          =   400
      Underline       =   0   'False
      Italic          =   0   'False
      Strikethrough   =   0   'False
   EndProperty
   LinkTopic       =   "Form1"
   ScaleHeight     =   7560
   ScaleWidth      =   13815
   StartUpPosition =   3  '´°¿ÚÈ±Ê¡
   Tag             =   "p@protocol=WM_DELETE_WINDOW"
   Begin VB.CommandButton cmdDeleteProfile 
      Caption         =   "Delete Profile"
      BeginProperty Font 
         Name            =   "Arial"
         Size            =   14.25
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   495
      Left            =   8160
      TabIndex        =   9
      Top             =   240
      Width           =   2535
   End
   Begin VB.OptionButton optMod2 
      Caption         =   "Mod2"
      Height          =   495
      Left            =   6240
      TabIndex        =   8
      Top             =   1080
      Width           =   1815
   End
   Begin VB.OptionButton optMod1 
      Caption         =   "Mod1"
      Height          =   495
      Left            =   4240
      TabIndex        =   7
      Top             =   1080
      Width           =   1815
   End
   Begin VB.OptionButton optCaps 
      Caption         =   "Caps"
      Height          =   495
      Left            =   2240
      TabIndex        =   6
      Top             =   1080
      Width           =   1815
   End
   Begin VB.OptionButton optNormal 
      Caption         =   "Normal"
      Height          =   495
      Left            =   240
      TabIndex        =   5
      Top             =   1080
      Value           =   -1  'True
      Width           =   1815
   End
   Begin VB.CommandButton cmdSaveXml 
      Caption         =   "Save Xml"
      BeginProperty Font 
         Name            =   "Arial"
         Size            =   14.25
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   495
      Left            =   11160
      TabIndex        =   4
      Top             =   240
      Width           =   2535
   End
   Begin VB.CommandButton cmdSaveProfile 
      Caption         =   "Save Profile"
      BeginProperty Font 
         Name            =   "Arial"
         Size            =   14.25
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   495
      Left            =   5160
      TabIndex        =   3
      Top             =   240
      Width           =   2535
   End
   Begin VB.ComboBox cmbProfile 
      BeginProperty Font 
         Name            =   "Arial"
         Size            =   14.25
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   450
      Left            =   1800
      Style           =   2  'Dropdown List
      TabIndex        =   2
      Top             =   240
      Width           =   3015
   End
   Begin VB.PictureBox canvas 
      BackColor       =   &H00C0E0FF&
      BeginProperty Font 
         Name            =   "Courier New"
         Size            =   15.75
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   5655
      Left            =   120
      ScaleHeight     =   5595
      ScaleWidth      =   13515
      TabIndex        =   0
      Top             =   1800
      Width           =   13575
   End
   Begin VB.Label lblProfile 
      Alignment       =   1  'Right Justify
      Caption         =   "Profile"
      BeginProperty Font 
         Name            =   "Arial"
         Size            =   14.25
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   120
      TabIndex        =   1
      Top             =   240
      Width           =   1455
   End
End
Attribute VB_Name = "kbmain"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Private Sub canvas_Click()

End Sub

Private Sub cmbProfile_Change()

End Sub

Private Sub cmdSaveProfileAs_Click()

End Sub

Private Sub cmdSaveXml_Click()

End Sub

Private Sub optCaps_Click()

End Sub

Private Sub optMod1_Click()

End Sub

Private Sub optMod2_Click()

End Sub

Private Sub optNormal_Click()

End Sub
