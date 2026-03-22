import httpx
from typing import Optional, Dict

class ViaCEPService:
    BASE_URL = "https://viacep.com.br/ws"

    @staticmethod
    async def get_address_by_cep(cep: str) -> Optional[Dict]:
        """
        Consome a API externa do ViaCEP para buscar dados de endereço.
        """
        # Remove caracteres não numéricos
        clean_cep = "".join(filter(str.isdigit, cep))
        
        if len(clean_cep) != 8:
            return None

        async with httpx.AsyncClient() as client:
            try:
                # Usando o nome da classe para acessar BASE_URL já que é staticmethod
                response = await client.get(f"{ViaCEPService.BASE_URL}/{clean_cep}/json/")
                if response.status_code == 200:
                    data = response.json()
                    if "erro" in data:
                        return None
                    return data
            except Exception:
                return None
        return None
