
# from reportlab.lib.pagesizes import A4
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.units import inch
# from reportlab.lib import colors
# from reportlab.lib.enums import TA_CENTER, TA_LEFT
# from io import BytesIO
# from models.tournament import Tournament
# from models.team import Team
# from models.player import Player
# from models.team_player import TeamPlayer
# from models.unsold_player import UnsoldPlayer
# from app.extensions import db

# class TournamentPDFExportService:
#     def __init__(self):
#         self.styles = getSampleStyleSheet()
#         self._setup_styles()

#     def _setup_styles(self):
#         self.title_style = ParagraphStyle(
#             'Title', parent=self.styles['Heading1'], fontSize=24,
#             alignment=TA_CENTER, textColor=colors.darkblue, spaceAfter=20
#         )
#         self.subtitle_style = ParagraphStyle(
#             'Subtitle', parent=self.styles['Heading2'], fontSize=16,
#             alignment=TA_CENTER, textColor=colors.darkgreen, spaceAfter=15
#         )
#         self.team_header_style = ParagraphStyle(
#             'TeamHeader', parent=self.styles['Heading3'], fontSize=14,
#             alignment=TA_LEFT, textColor=colors.darkblue, leftIndent=10,
#             fontName='Helvetica-Bold', spaceAfter=10
#         )
#         self.normal_style = ParagraphStyle(
#             'Normal', parent=self.styles['Normal'], fontSize=11, spaceAfter=8
#         )
#         self.cell_style = ParagraphStyle(
#             'cellStyle', parent=self.styles['Normal'], fontSize=10,
#             leading=12, alignment=TA_LEFT, wordWrap='CJK'
#         )

#     def export_auction_summary(self, tournament_id: str):
#         """Export completed auction details as PDF"""
#         tournament = Tournament.query.get(tournament_id)
#         if not tournament:
#             return None, "Tournament not found"

#         buffer = BytesIO()
#         doc = SimpleDocTemplate(buffer, pagesize=A4,
#                                 rightMargin=50, leftMargin=50,
#                                 topMargin=50, bottomMargin=50)
#         story = []

#         # Tournament Title
#         story.append(Paragraph(f"{tournament.name} - Auction Summary", self.title_style))
#         story.append(Spacer(1, 15))

#         # Tournament Info
#         info_table_data = [
#             ["Venue:", tournament.venue],
#             ["Tournament Type:", tournament.tournament_type or "N/A"],
#             ["Start Date:", tournament.start_date.strftime("%B %d, %Y")],
#             ["End Date:", tournament.end_date.strftime("%B %d, %Y")],
#         ]
#         info_table = Table(info_table_data, colWidths=[2.5*inch, 3*inch])
#         info_table.setStyle(TableStyle([
#             ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
#             ('GRID', (0,0), (-1,-1), 1, colors.black),
#             ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
#             ('FONTSIZE', (0,0), (-1,-1), 11),
#         ]))
#         story.append(info_table)
#         story.append(Spacer(1, 20))

#         # Fetch teams
#         teams = Team.query.filter_by(tournament_id=tournament_id).all()

#         for team in teams:
#             story.append(Paragraph(f"🏏 {team.team_name} | Owner: {team.owner_name}", self.team_header_style))
#             story.append(Spacer(1, 5))

#             # Fetch players
#             players = TeamPlayer.query.filter_by(team_id=team.id, tournament_id=tournament_id).all()
#             if players:
#                 table_data = [["Sr.", "Player Name", "Flat No", "Age", "Playing Style", "Category", "Bid Amount", "Role"]]
                
#                 # Pre-fetch players to avoid N+1 query
#                 player_ids = [tp.player_id for tp in players]
#                 player_map = {p.id: p for p in Player.query.filter(Player.id.in_(player_ids)).all()}

#                 for idx, tp in enumerate(players, 1):
#                     player = player_map.get(tp.player_id)
#                     if not player:
#                         continue

#                     style_list = []
#                     if player.bowler_type:
#                         style_list.append(f"Bowler({player.bowler_type})")
#                     if player.batter_type:
#                         style_list.append(f"Batter({player.batter_type})")
#                     style_str = ", ".join(style_list) if style_list else "N/A"

#                     # Determine role
#                     full_name = f"{player.name} {player.last_name}".lower()
#                     owner_name = team.owner_name.lower()
#                     if full_name == owner_name:
#                         role = "Owner"
#                     elif idx == 1:
#                         role = "Captain"
#                     else:
#                         role = "Player"

#                     table_data.append([
#                         str(idx),
#                         Paragraph(f"{player.name} {player.last_name}", self.cell_style),
#                         player.flat_no,
#                         str(player.age),
#                         Paragraph(style_str, self.cell_style),
#                         player.category or "",
#                         f"₹{tp.bid_amount:,.2f}",
#                         role
#                     ])

#                 player_table = Table(table_data,
#                                      colWidths=[0.4*inch, 1.8*inch, 0.7*inch, 0.5*inch, 1.5*inch, 0.7*inch, 1*inch, 0.7*inch],
#                                      repeatRows=1)
#                 player_table.setStyle(TableStyle([
#                     ('BACKGROUND', (0,0), (-1,0), colors.darkgreen),
#                     ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
#                     ('ALIGN', (0,0), (-1,-1), 'CENTER'),
#                     ('GRID', (0,0), (-1,-1), 1, colors.black),
#                     ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.lightgrey]),
#                     ('ALIGN', (1,1), (1,-1), 'LEFT'),
#                     ('ALIGN', (4,1), (4,-1), 'LEFT')
#                 ]))
#                 player_table.splitByRow = True
#                 story.append(player_table)
#                 story.append(Spacer(1, 15))
#             else:
#                 story.append(Paragraph("No players assigned.", self.normal_style))

#         # Unsold players
#         story.append(PageBreak())
#         story.append(Paragraph("Waitlist (Unsold Players)", self.subtitle_style))
#         unsold_players = UnsoldPlayer.query.filter_by(tournament_id=tournament_id).all()
#         if unsold_players:
#             table_data = [["Sr.", "Player Name", "Flat No", "Age", "Playing Style", "Category"]]
#             player_ids = [up.player_id for up in unsold_players]
#             player_map = {p.id: p for p in Player.query.filter(Player.id.in_(player_ids)).all()}

#             for idx, up in enumerate(unsold_players, 1):
#                 player = player_map.get(up.player_id)
#                 if not player:
#                     continue
#                 style_list = []
#                 if player.bowler_type:
#                     style_list.append(f"Bowler({player.bowler_type})")
#                 if player.batter_type:
#                     style_list.append(f"Batter({player.batter_type})")
#                 style_str = ", ".join(style_list) if style_list else "N/A"

#                 table_data.append([
#                     str(idx),
#                     Paragraph(f"{player.name} {player.last_name}", self.cell_style),
#                     player.flat_no,
#                     str(player.age),
#                     Paragraph(style_str, self.cell_style),
#                     player.category or ""
#                 ])

#             unsold_table = Table(table_data,
#                                  colWidths=[0.4*inch, 1.8*inch, 0.7*inch, 0.5*inch, 1.5*inch, 0.7*inch],
#                                  repeatRows=1)
#             unsold_table.setStyle(TableStyle([
#                 ('BACKGROUND', (0,0), (-1,0), colors.darkred),
#                 ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
#                 ('ALIGN', (0,0), (-1,-1), 'CENTER'),
#                 ('GRID', (0,0), (-1,-1), 1, colors.black),
#                 ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.lightgrey]),
#                 ('ALIGN', (1,1), (1,-1), 'LEFT'),
#                 ('ALIGN', (4,1), (4,-1), 'LEFT')
#             ]))
#             unsold_table.splitByRow = True
#             story.append(unsold_table)
#         else:
#             story.append(Paragraph("No unsold players.", self.normal_style))

#         # Build PDF
#         doc.build(story)
#         buffer.seek(0)
#         return buffer, None


from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from models.tournament import Tournament
from models.team import Team
from models.player import Player
from models.team_player import TeamPlayer
from models.unsold_player import UnsoldPlayer
from app.extensions import db

class TournamentPDFExportService:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_styles()

    def _setup_styles(self):
        # Main Tournament Heading
        self.title_style = ParagraphStyle(
            'Title', parent=self.styles['Heading1'], fontSize=24,
            alignment=TA_CENTER, textColor=colors.darkred, spaceAfter=20
        )
        # Subheaders (like Unsold Players)
        self.subtitle_style = ParagraphStyle(
            'Subtitle', parent=self.styles['Heading2'], fontSize=16,
            alignment=TA_CENTER, textColor=colors.red, spaceAfter=15
        )
        self.team_header_style = ParagraphStyle(
            'TeamHeader', parent=self.styles['Heading3'], fontSize=14,
            alignment=TA_LEFT, textColor=colors.darkblue, leftIndent=10,
            fontName='Helvetica-Bold', spaceAfter=10
        )
        self.normal_style = ParagraphStyle(
            'Normal', parent=self.styles['Normal'], fontSize=11, spaceAfter=8
        )
        self.cell_style = ParagraphStyle(
            'cellStyle', parent=self.styles['Normal'], fontSize=10,
            leading=12, alignment=TA_LEFT, wordWrap='CJK'
        )

    def export_auction_summary(self, tournament_id: str):
        """Export completed auction details as PDF"""
        tournament = Tournament.query.get(tournament_id)
        if not tournament:
            return None, "Tournament not found"

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4,
                                rightMargin=50, leftMargin=50,
                                topMargin=50, bottomMargin=50)
        story = []

        # Tournament Title (Main Heading)
        story.append(Paragraph(f"{tournament.name}", self.title_style))
        story.append(Spacer(1, 15))

        # Tournament Info
        info_table_data = [
            ["Venue:", tournament.venue],
            ["Tournament Type:", tournament.tournament_type or "N/A"],
            ["Start Date:", tournament.start_date.strftime("%B %d, %Y")],
            ["End Date:", tournament.end_date.strftime("%B %d, %Y")],
        ]
        info_table = Table(info_table_data, colWidths=[2.5*inch, 3*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightcoral),  # Slight red shade for headers
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 11),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 20))

        # Fetch teams
        teams = Team.query.filter_by(tournament_id=tournament_id).all()

        for team in teams:
            story.append(Paragraph(f"🏏 {team.team_name} | Owner: {team.owner_name}", self.team_header_style))
            story.append(Spacer(1, 5))

            # Fetch players
            players = TeamPlayer.query.filter_by(team_id=team.id, tournament_id=tournament_id).all()
            if players:
                table_data = [["Sr.", "Player Name", "Flat No", "Age", "Playing Style", "Category", "Bid Amount", "Role"]]
                
                # Pre-fetch players
                player_ids = [tp.player_id for tp in players]
                player_map = {p.id: p for p in Player.query.filter(Player.id.in_(player_ids)).all()}

                for idx, tp in enumerate(players, 1):
                    player = player_map.get(tp.player_id)
                    if not player:
                        continue

                    style_list = []
                    if player.bowler_type:
                        style_list.append(f"Bowler({player.bowler_type})")
                    if player.batter_type:
                        style_list.append(f"Batter({player.batter_type})")
                    style_str = ", ".join(style_list) if style_list else "N/A"

                    # Determine role
                    full_name = f"{player.name} {player.last_name}".lower()
                    owner_name = team.owner_name.lower()
                    if full_name == owner_name:
                        role = "Owner"
                    elif idx == 1:
                        role = "Captain"
                    else:
                        role = "Player"

                    table_data.append([
                        str(idx),
                        Paragraph(f"{player.name} {player.last_name}", self.cell_style),
                        player.flat_no,
                        str(player.age),
                        Paragraph(style_str, self.cell_style),
                        player.category or "",
                        f"₹{tp.bid_amount:,.2f}",
                        role
                    ])

                player_table = Table(table_data,
                                     colWidths=[0.4*inch, 1.8*inch, 0.7*inch, 0.5*inch, 1.5*inch, 0.7*inch, 1*inch, 0.7*inch],
                                     repeatRows=1)
                player_table.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.darkgreen),
                    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                    ('GRID', (0,0), (-1,-1), 1, colors.black),
                    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.lightgrey]),
                    ('ALIGN', (1,1), (1,-1), 'LEFT'),
                    ('ALIGN', (4,1), (4,-1), 'LEFT')
                ]))
                player_table.splitByRow = True
                story.append(player_table)
                story.append(Spacer(1, 15))
            else:
                story.append(Paragraph("No players assigned.", self.normal_style))

        # Unsold players
        story.append(PageBreak())
        story.append(Paragraph("Waitlist (Unsold Players)", self.subtitle_style))
        unsold_players = UnsoldPlayer.query.filter_by(tournament_id=tournament_id).all()
        if unsold_players:
            table_data = [["Sr.", "Player Name", "Flat No", "Age", "Playing Style", "Category"]]
            player_ids = [up.player_id for up in unsold_players]
            player_map = {p.id: p for p in Player.query.filter(Player.id.in_(player_ids)).all()}

            for idx, up in enumerate(unsold_players, 1):
                player = player_map.get(up.player_id)
                if not player:
                    continue
                style_list = []
                if player.bowler_type:
                    style_list.append(f"Bowler({player.bowler_type})")
                if player.batter_type:
                    style_list.append(f"Batter({player.batter_type})")
                style_str = ", ".join(style_list) if style_list else "N/A"

                table_data.append([
                    str(idx),
                    Paragraph(f"{player.name} {player.last_name}", self.cell_style),
                    player.flat_no,
                    str(player.age),
                    Paragraph(style_str, self.cell_style),
                    player.category or ""
                ])

            unsold_table = Table(table_data,
                                 colWidths=[0.4*inch, 1.8*inch, 0.7*inch, 0.5*inch, 1.5*inch, 0.7*inch],
                                 repeatRows=1)
            unsold_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.red),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('GRID', (0,0), (-1,-1), 1, colors.black),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.lightgrey]),
                ('ALIGN', (1,1), (1,-1), 'LEFT'),
                ('ALIGN', (4,1), (4,-1), 'LEFT')
            ]))
            unsold_table.splitByRow = True
            story.append(unsold_table)
        else:
            story.append(Paragraph("No unsold players.", self.normal_style))

        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer, None
