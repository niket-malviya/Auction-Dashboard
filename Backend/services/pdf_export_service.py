from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from models.tournament import Tournament
from models.team import Team
from models.player import Player
from models.team_player import TeamPlayer
from app.extensions import db
import uuid

class TournamentPDFExportService:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom paragraph styles for the PDF"""
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=28,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        # Subtitle style
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=18,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.darkgreen
        )
        
        # Team header style
        self.team_header_style = ParagraphStyle(
            'TeamHeader',
            parent=self.styles['Heading3'],
            fontSize=18,
            spaceAfter=15,
            alignment=TA_LEFT,
            textColor=colors.darkblue,
            leftIndent=20,
            fontName='Helvetica-Bold'
        )
        
        # Normal text style
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=12
        )
    
    def export_tournament_details(self, tournament_id):
        """Export tournament details with team and player information organized by teams"""
        # Get tournament details
        tournament = Tournament.query.get(tournament_id)
        if not tournament:
            return None, "Tournament not found"
        
        # Create PDF buffer
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
        
        # Build PDF content
        story = []
        
        # Add main tournament title
        title = Paragraph(f"{tournament.name}", self.title_style)
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Add tournament information
        tournament_info = [
            ["Sport Type:", tournament.sport_type.sport_name if tournament.sport_type else "N/A"],
            ["Tournament Type:", tournament.tournament_type],
            ["Start Date:", tournament.start_date.strftime("%B %d, %Y") if tournament.start_date else "N/A"],
            ["End Date:", tournament.end_date.strftime("%B %d, %Y") if tournament.end_date else "N/A"],
            ["Venue:", tournament.venue]
        ]
        
        tournament_table = Table(tournament_info, colWidths=[2*inch, 4*inch])
        tournament_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(tournament_table)
        story.append(Spacer(1, 30))
        
        # Get all teams
        teams = Team.query.all()
        
        # Get all team-player assignments for this tournament
        team_players = TeamPlayer.query.filter_by(tournament_id=tournament_id).all()
        
        # Group players by team
        team_player_map = {}
        for tp in team_players:
            if tp.team_id not in team_player_map:
                team_player_map[tp.team_id] = []
            team_player_map[tp.team_id].append(tp)
        
        # Create content for each team
        for team in teams:
            # Team header with owner and captain info
            team_header = Paragraph(f"🏏 {team.team_name} | Owner: {team.owner_name}", self.team_header_style)
            story.append(team_header)
            story.append(Spacer(1, 10))

            # Add team image if img_url is present
            if team.img_url:
                try:
                    if team.img_url.startswith('http'):
                        # If it's a URL, just show the URL as text (since reportlab can't fetch remote images)
                        story.append(Paragraph(f"<b>Team Image:</b> <a href='{team.img_url}'>{team.img_url}</a>", self.normal_style))
                    else:
                        # If it's a local file path, try to embed the image
                        story.append(Image(team.img_url, width=1.2*inch, height=1.2*inch))
                    story.append(Spacer(1, 8))
                except Exception:
                    story.append(Paragraph(f"<b>Team Image:</b> {team.img_url}", self.normal_style))
                    story.append(Spacer(1, 8))
            
            # Team budget information
            budget_info = [
                ["Total Budget:", f"₹{team.total_amount:,.2f}"],
                ["Remaining Budget:", f"₹{team.remaining_amount:,.2f}"],
                ["Max Players:", str(team.max_players)]
            ]
            
            budget_table = Table(budget_info, colWidths=[2*inch, 2*inch])
            budget_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey)
            ]))
            
            story.append(budget_table)
            story.append(Spacer(1, 15))
            
            # Get players for this team
            assignments = team_player_map.get(team.id, [])
            
            if assignments:
                # Player table headers
                player_data = [["Sr. No.", "Player Name", "Flat No.", "Age", "Playing Style", "Category", "Bid Amount", "Role"]]
                
                for i, assignment in enumerate(assignments, 1):
                    player = Player.query.get(assignment.player_id)
                    if player:
                        # Determine playing style
                        playing_style = []
                        if player.bowler_type:
                            playing_style.append(f"Bowler ({player.bowler_type})")
                        if player.batter_type:
                            playing_style.append(f"Batter ({player.batter_type})")
                        playing_style_str = ", ".join(playing_style) if playing_style else "N/A"
                        
                        # Determine player role (you can customize this based on your logic)
                        role = "Player"
                        if i == 1:  # First player could be captain
                            role = "Captain"
                        elif team.owner_name.lower() in player.name.lower() or team.owner_name.lower() in player.last_name.lower():
                            role = "Owner"
                        
                        player_data.append([
                            str(i),
                            f"{player.name} {player.last_name}",
                            player.flat_no,
                            str(player.age),
                            playing_style_str,
                            player.category,
                            f"₹{assignment.bid_amount:,.2f}",
                            role
                        ])
                
                # Create player table
                player_table = Table(player_data, colWidths=[0.5*inch, 1.8*inch, 0.7*inch, 0.5*inch, 1.3*inch, 0.7*inch, 1*inch, 0.7*inch])
                player_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightcyan),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
                    ('ALIGN', (1, 1), (1, -1), 'LEFT'),  # Player name left-aligned
                    ('ALIGN', (4, 1), (4, -1), 'LEFT'),  # Playing style left-aligned
                ]))
                
                story.append(player_table)
            else:
                no_players = Paragraph("No players assigned to this team", self.normal_style)
                story.append(no_players)
            
            story.append(Spacer(1, 25))
        
        # Add unsold players section at the end
        story.append(PageBreak())
        unsold_header = Paragraph("Unsold Players", self.subtitle_style)
        story.append(unsold_header)
        story.append(Spacer(1, 15))
        
        # Get unsold players for this tournament
        from models.unsold_player import UnsoldPlayer
        unsold_players = UnsoldPlayer.query.filter_by(tournament_id=tournament_id).all()
        
        if unsold_players:
            unsold_data = [["Sr. No.", "Player Name", "Flat No.", "Age", "Playing Style", "Category"]]
            
            for i, unsold in enumerate(unsold_players, 1):
                player = Player.query.get(unsold.player_id)
                if player:
                    playing_style = []
                    if player.bowler_type:
                        playing_style.append(f"Bowler ({player.bowler_type})")
                    if player.batter_type:
                        playing_style.append(f"Batter ({player.batter_type})")
                    playing_style_str = ", ".join(playing_style) if playing_style else "N/A"
                    
                    unsold_data.append([
                        str(i),
                        f"{player.name} {player.last_name}",
                        player.flat_no,
                        str(player.age),
                        playing_style_str,
                        player.category
                    ])
            
            unsold_table = Table(unsold_data, colWidths=[0.6*inch, 2.5*inch, 0.8*inch, 0.6*inch, 2*inch, 0.8*inch])
            unsold_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkred),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightcoral),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
                ('ALIGN', (1, 1), (1, -1), 'LEFT'),  # Player name left-aligned
                ('ALIGN', (4, 1), (4, -1), 'LEFT'),  # Playing style left-aligned
            ]))
            
            story.append(unsold_table)
        else:
            no_unsold = Paragraph("No unsold players", self.normal_style)
            story.append(no_unsold)
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        
        return buffer, None
    
    def export_tournament_summary(self, tournament_id):
        """Export a summary version of tournament details"""
        # Get tournament details
        tournament = Tournament.query.get(tournament_id)
        if not tournament:
            return None, "Tournament not found"
        
        # Create PDF buffer
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
        
        # Build PDF content
        story = []
        
        # Add title
        title = Paragraph(f"{tournament.name} - Summary Report", self.title_style)
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Get statistics
        total_teams = Team.query.count()
        total_players = Player.query.filter_by(tournament_id=tournament_id).count()
        assigned_players = TeamPlayer.query.filter_by(tournament_id=tournament_id).count()
        unsold_players = db.session.query(UnsoldPlayer).filter_by(tournament_id=tournament_id).count()
        
        # Summary statistics
        summary_data = [
            ["Metric", "Count"],
            ["Total Teams", str(total_teams)],
            ["Total Players", str(total_players)],
            ["Assigned Players", str(assigned_players)],
            ["Unsold Players", str(unsold_players)],
            ["Success Rate", f"{(assigned_players/total_players*100):.1f}%" if total_players > 0 else "0%"]
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(summary_table)
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        
        return buffer, None
