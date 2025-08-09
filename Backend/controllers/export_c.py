from flask import send_file
from services.pdf_export_service import TournamentPDFExportService
from models.tournament import Tournament
from io import BytesIO

def export_tournament_pdf(tournament_id, export_type="details"):
    """Export tournament details as PDF"""
    # Check if tournament exists
    tournament = Tournament.query.get(tournament_id)
    if not tournament:
        return {'message': 'Tournament not found'}, 404
    
    # Create PDF export service
    pdf_service = TournamentPDFExportService()
    
    try:
        if export_type == "summary":
            buffer, error = pdf_service.export_tournament_summary(tournament_id)
        else:
            buffer, error = pdf_service.export_tournament_details(tournament_id)
        
        if error:
            return {'message': error}, 400
        
        # Prepare file for download
        buffer.seek(0)
        
        # Generate filename
        filename = f"tournament_{tournament.name.replace(' ', '_')}_{export_type}.pdf"
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return {'message': f'Error generating PDF: {str(e)}'}, 500

def get_export_options(tournament_id):
    """Get available export options for a tournament"""
    tournament = Tournament.query.get(tournament_id)
    if not tournament:
        return {'message': 'Tournament not found'}, 404
    
    return {
        'tournament_id': tournament_id,
        'tournament_name': tournament.name,
        'export_options': [
            {
                'type': 'details',
                'name': 'Full Tournament Details',
                'description': 'Complete tournament information with all teams and players'
            },
            {
                'type': 'summary',
                'name': 'Tournament Summary',
                'description': 'Brief overview with statistics'
            }
        ]
    }, 200 