package org.springframework.samples.petclinic.owner;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

import java.util.Optional;

import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;

/**
 * Caso de prueba funcional para el método showOwner() del controlador OwnerController. Se
 * valida el comportamiento del endpoint GET /owners/{ownerId}.
 */
@SpringBootTest
@AutoConfigureMockMvc
class OwnerControllerShowOwnerTestIA {

	@Autowired
	private MockMvc mockMvc;

	// Se simula el repositorio o servicio de propietarios
	@MockBean
	private OwnerRepository owners;

	/**
	 * Caso exitoso: el propietario existe. Se espera código 200, vista
	 * "owners/ownerDetails" y que el atributo "owner" esté presente en el modelo.
	 */
	@Test
	void shouldReturnOwnerDetailsWhenOwnerExists() throws Exception {
		// Arrange: se prepara un propietario simulado
		Owner owner = new Owner();
		owner.setId(1);
		owner.setFirstName("John");
		owner.setLastName("Doe");

		Mockito.when(owners.findById(1)).thenReturn(Optional.of(owner));

		// Act & Assert: se ejecuta la solicitud y se verifican los resultados
		mockMvc.perform(get("/owners/{ownerId}", 1))
			.andExpect(status().isOk()) // Verifica que el HTTP status sea 200
			.andExpect(view().name("owners/ownerDetails")) // Verifica la vista retornada
			.andExpect(model().attributeExists("owner")) // Verifica que el modelo tenga
															// el atributo "owner"
			.andExpect(model().attribute("owner", owner)); // Verifica que el objeto
															// "owner" sea el mismo
	}

	/**
	 * Caso alternativo: el propietario NO existe. Se espera un error 4xx debido a la
	 * excepción IllegalArgumentException.
	 */
	@Test
	void shouldReturnClientErrorWhenOwnerNotFound() throws Exception {
		// Arrange: el repositorio no encuentra al propietario
		Mockito.when(owners.findById(99)).thenReturn(Optional.empty());

		// Act & Assert: se espera una excepción y un código de error 4xx
		mockMvc.perform(get("/owners/{ownerId}", 99)).andExpect(status().is4xxClientError());
	}

}
