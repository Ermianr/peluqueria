from datetime import datetime, timezone
from io import BytesIO
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from peluqueria.api.db.db_connect import db
from peluqueria.api.models.user import UserInDBResponse as User
from peluqueria.api.routers.auth import get_current_user

router = APIRouter()


@router.get("/dashboard-report")
async def generate_dashboard_report(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.role != "employee":
        raise HTTPException(
            status_code=403, detail="No tienes permisos para generar reportes"
        )

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=24,
        spaceAfter=30,
        alignment=1,
        textColor=colors.black,
    )

    subtitle_style = ParagraphStyle(
        "CustomSubtitle",
        parent=styles["Heading2"],
        fontSize=16,
        spaceAfter=20,
        textColor=colors.darkblue,
    )

    normal_style = ParagraphStyle(
        "CustomNormal",
        parent=styles["Normal"],
        fontSize=12,
        spaceAfter=12,
        textColor=colors.black,
    )

    title = Paragraph("Reporte del Dashboard - Peluquería Divine", title_style)
    story.append(title)

    date_info = Paragraph(
        f"Fecha de generación: {datetime.now(tz=timezone.utc).strftime('%d/%m/%Y %H:%M')}",
        normal_style,
    )
    story.append(date_info)
    story.append(Spacer(1, 20))

    try:
        total_appointments = await db.appointments.count_documents({})

        today = datetime.now(tz=timezone.utc).date().isoformat()
        today_appointments = await db.appointments.count_documents(
            {"date": {"$regex": f"^{today}"}}
        )

        total_users = await db.users.count_documents({})

        total_services = await db.services.count_documents({})

        metrics_title = Paragraph("Métricas Generales", subtitle_style)
        story.append(metrics_title)

        metrics_data = [
            ["Métrica", "Valor"],
            ["Total de Citas", str(total_appointments)],
            ["Citas de Hoy", str(today_appointments)],
            ["Total de Usuarios", str(total_users)],
            ["Total de Servicios", str(total_services)],
        ]

        metrics_table = Table(metrics_data, colWidths=[2.5 * inch, 1.5 * inch])
        metrics_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 14),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
        )

        story.append(metrics_table)
        story.append(Spacer(1, 30))

        pipeline = [
            {
                "$lookup": {
                    "from": "services",
                    "localField": "service_id",
                    "foreignField": "_id",
                    "as": "service",
                }
            },
            {"$unwind": "$service"},
            {"$group": {"_id": "$service.name", "total_appointments": {"$sum": 1}}},
            {"$sort": {"total_appointments": -1}},
            {"$limit": 5},
        ]

        services_stats = []
        async for doc in await db.appointments.aggregate(pipeline):
            services_stats.append((doc["_id"], doc["total_appointments"]))

        if services_stats:
            services_title = Paragraph("Servicios Más Solicitados", subtitle_style)
            story.append(services_title)

            services_data = [["Servicio", "Total de Citas"]]
            for service_name, count in services_stats:
                services_data.append([service_name, str(count)])

            services_table = Table(services_data, colWidths=[3 * inch, 1 * inch])
            services_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 12),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.lightblue),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ]
                )
            )

            story.append(services_table)
            story.append(Spacer(1, 30))

    except Exception as e:
        error_msg = Paragraph(f"Error al generar el reporte: {str(e)}", normal_style)
        story.append(error_msg)

    footer_text = Paragraph(
        "Generado por Sistema de Gestión - Peluquería Divine", normal_style
    )
    story.append(Spacer(1, 50))
    story.append(footer_text)

    doc.build(story)

    buffer.seek(0)
    pdf_content = buffer.read()
    buffer.close()

    filename = f"dashboard_report_{datetime.now(tz=timezone.utc).strftime('%Y%m%d_%H%M%S')}.pdf"

    return Response(
        content=pdf_content,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
        },
    )
